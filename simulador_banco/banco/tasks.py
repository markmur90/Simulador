# tasks.py (usando Celery)

from celery import shared_task
from django.db import transaction
from simulator.models import Transfer, DebtorAccount
import requests

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
        transfer.settings.SIMULATOR_NOTIFY_URL,
        json=payload,
        timeout=5
    )
