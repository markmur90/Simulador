"""Tareas asincrónicas de la aplicación Banco."""

import asyncio
import requests
# from telegram import Bot

import openai
# from celery import shared_task
from django.conf import settings
from django.db import transaction

from banco.models import DebtorAccount, Transfer


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

    # Envolver la llamada asíncrona en ``asyncio.run`` para no usar
    # ``await`` directamente dentro del worker de Celery
    async def _do_chat():
        return await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

    try:
        resp = asyncio.run(_do_chat())
        return resp.choices[0].message.content.strip()
    except Exception:
        return "Sin análisis disponible"


def send_telegram_notification(message: str) -> None:
    """Envía un mensaje por Telegram si están configuradas las credenciales."""
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", None)
    if not (token and chat_id):
        return
    try:
        # Bot(token=token).send_message(chat_id=chat_id, text=message)
        pass # Temporarily disabled
    except Exception:
        # Podríamos loguear el error para auditoría
        pass


# @shared_task
def process_transfer_task(transfer_id):
    """Procesa una transferencia en segundo plano."""
    from banco.models import Transfer
    
    try:
        transfer = Transfer.objects.get(id=transfer_id)
        
        # Simular procesamiento
        transfer.status = 'ACSP'
        transfer.save()
            
    except Transfer.DoesNotExist:
        logger.error(f"Transferencia {transfer_id} no encontrada")
    except Exception as e:
        logger.error(f"Error procesando transferencia {transfer_id}: {str(e)}")