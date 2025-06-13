# tasks.py (usando Celery)

from celery import shared_task
from django.db import transaction
from banco.models import Transfer, DebtorAccount
from django.conf import settings
import requests
import openai
from telegram import Bot

def analyze_transfer(transfer: Transfer) -> str:
    """Use OpenAI to analyze a transfer."""
    try:
        openai.api_key = settings.OPENAI_API_KEY
    except AttributeError:
        return "Sin análisis disponible"

    prompt = (
        f"Analiza la transferencia de {transfer.debtor.name} "
        f"por {transfer.instructed_amount} {transfer.currency} "
        f"hacia {transfer.creditor.name}."
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return "Sin análisis disponible"


def send_telegram_notification(message: str) -> None:
    """Send a Telegram message if credentials are present."""
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", None)
    if not token or not chat_id:
        return
    try:
        Bot(token=token).send_message(chat_id=chat_id, text=message)
    except Exception:
        pass
    

@shared_task
def process_transfer_task(transfer_id: int):
    """
    A los 5 minutos, procesa la transferencia:
     - resta el monto del DebtorAccount.balance
     - actualiza status a 'ACSC'
     - notifica a la API externa
    """
    try:
        transfer = Transfer.objects.select_related('debtor_account').get(id=transfer_id)
    except Transfer.DoesNotExist:
        return

    if transfer.status != 'PDNG':
        return

    with transaction.atomic():
        acct = DebtorAccount.objects.select_for_update().get(id=transfer.debtor_account_id)

        # 1) Verificar fondos
        if acct.balance < transfer.instructed_amount:
            transfer.status = 'RJCT'
            transfer.save(update_fields=['status'])
            return

        # 2) Descontar y actualizar
        acct.balance -= transfer.instructed_amount
        acct.save(update_fields=['balance'])

        transfer.status = 'ACSC'
        transfer.save(update_fields=['status'])

    # 3) Notificar a la API externa
    payload = {
        "payment_id": transfer.payment_id,
        "status": transfer.status,
        "debtor_account": acct.iban,
        "amount": str(transfer.instructed_amount),
    }
    # URL configurada en settings.SIMULATOR_NOTIFY_URL
    requests.post(
        settings.SIMULATOR_NOTIFY_URL,
        json=payload,
        timeout=5
    )

    # 4) Análisis y notificación externa
    analysis = analyze_transfer(transfer)
    send_telegram_notification(f"Transferencia {transfer.payment_id}: {analysis}")