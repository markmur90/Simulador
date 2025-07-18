"""Tareas asincrónicas de la aplicación Banco."""

import asyncio
import requests
from telegram import Bot

import openai
from celery import shared_task
from django.conf import settings
from django.db import transaction

from banco.models import DebtorAccount, Transfer, AccountMovement


def analyze_transfer(transfer: Transfer) -> str:
    """Usa OpenAI para analizar una transferencia de forma síncrona."""
    api_key = getattr(settings, "OPENAI_API_KEY", None)
    if not api_key:
        return "Sin análisis disponible"
    openai.api_key = api_key

    prompt = (
        f"Analiza la transferencia de {transfer.debtor.name} "
        f"por {transfer.instructed_amount} {transfer.currency} "
        f"hacia {transfer.creditor.name}."
    )

    try:
        # Envolver la llamada asíncrona en ``asyncio.run`` para no usar
        # ``await`` directamente dentro del worker de Celery
        async def _do_chat():
            return await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

        resp = asyncio.run(_do_chat())
        return resp.choices[0].message.content.strip()
    except Exception:
        return "Sin análisis disponible"


@shared_task
def process_transfer_task(transfer_id: int):
    """
    Procesa una transferencia pendiente:
     1) Verifica fondos
     2) Registra el movimiento de salida
     3) Actualiza status
     4) Notifica a la API externa
     5) Realiza análisis con OpenAI y notifica por Telegram
    """
    try:
        transfer = (
            Transfer.objects.select_related('debtor_account')
            .get(id=transfer_id)
        )
    except Transfer.DoesNotExist:
        return

    if transfer.status != 'PDNG':
        return

    # Bloque atómico para evitar race conditions
    with transaction.atomic():
        acct = (
            DebtorAccount.objects.select_for_update()
            .get(id=transfer.debtor_account.id)
        )

        # 1) Verificar fondos
        if acct.balance < transfer.instructed_amount:
            transfer.status = 'RJCT'
            transfer.save(update_fields=['status'])
            
            # Registrar el intento fallido
            AccountMovement.objects.create(
                account=acct,
                tipo='PAYMENT',
                monto=transfer.instructed_amount,
                descripcion=f'Transferencia rechazada por fondos insuficientes: {transfer.payment_id}'
            )
            return

        # 2) Registrar movimiento de salida
        AccountMovement.objects.create(
            account=acct,
            tipo='PAYMENT',
            monto=transfer.instructed_amount,
            descripcion=f'Transferencia enviada a {transfer.creditor.name} - ID: {transfer.payment_id}'
        )

        # 3) Actualizar estado
        transfer.status = 'ACCP'
        transfer.save(update_fields=['status'])

        # 4) Registrar en el log
        LogTransferencia.objects.create(
            registro=transfer.payment_id,
            tipo_log='TRANSFER',
            contenido=f'Transferencia procesada exitosamente'
        )

        # 5) Notificar por Telegram si está configurado
        if hasattr(settings, 'TELEGRAM_BOT_TOKEN') and hasattr(settings, 'TELEGRAM_CHAT_ID'):
            try:
                bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                message = (
                    f"🔄 Nueva transferencia procesada\n"
                    f"ID: {transfer.payment_id}\n"
                    f"De: {transfer.debtor.name}\n"
                    f"A: {transfer.creditor.name}\n"
                    f"Monto: {transfer.instructed_amount} {transfer.currency}\n"
                    f"Estado: {transfer.status}"
                )
                asyncio.run(bot.send_message(
                    chat_id=settings.TELEGRAM_CHAT_ID,
                    text=message
                ))
            except Exception as e:
                # No fallar si la notificación falla
                print(f"Error enviando notificación Telegram: {e}")

        # 6) Realizar análisis con OpenAI
        try:
            analysis = analyze_transfer(transfer)
            if analysis != "Sin análisis disponible":
                LogTransferencia.objects.create(
                    registro=transfer.payment_id,
                    tipo_log='ANALYSIS',
                    contenido=analysis
                )
        except Exception as e:
            print(f"Error realizando análisis OpenAI: {e}")