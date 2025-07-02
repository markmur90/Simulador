import datetime
from typing import Any, Dict
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from banco.models import Transfer, DebtorAccount, OTPChallenge
from banco.tasks import process_transfer_task


class TransferService:
    """
    Servicio para ingestar y procesar Transfers respetando:
     - idempotencia por payment_id
     - rate-limit (5 en 5 minutos)
     - procesamiento diferido a los 5 minutos
    """
    RATE_LIMIT = 5
    WINDOW_MINUTES = 5

    @staticmethod
    @transaction.atomic
    def ingest_transfer(data: Dict[str, Any]) -> Transfer:
        """
        Inserta o rechaza una transferencia según reglas y registra todos los datos enviados desde Heroku.
        """

        # 1) Determinar payment_id e Idempotency
        payment_id = data.pop("Idempotency-Id", None) or data.get("payment_id")
        if not payment_id:
            raise ValidationError("'payment_id' requerido")
        data["payment_id"] = payment_id

        # Idempotencia
        existing = Transfer.objects.filter(payment_id=payment_id).first()
        if existing:
            return existing

        # 2) Rate-limit por cuenta deudora
        window_start = timezone.now() - datetime.timedelta(
            minutes=TransferService.WINDOW_MINUTES
        )
        recent_count = Transfer.objects.filter(
            debtor_account_id=data["debtor_account_id"],
            created_at__gte=window_start
        ).count()
        if recent_count >= TransferService.RATE_LIMIT:
            transfer = Transfer.objects.create(status='RJCT', **data)
            return transfer

        # 3) Crear transferencia en estado PDNG
        data["status"] = 'PDNG'
        transfer = Transfer.objects.create(**data)

        # 4) Programar procesamiento
        process_transfer_task.apply_async(
            args=[transfer.id],
            countdown=TransferService.WINDOW_MINUTES * 60
        )

        return transfer


def confirm_transfer(payment_id, otp_input, user):
    challenge = OTPChallenge.objects.get(payment_id=payment_id, otp=otp_input, status="CREATED")
    challenge.status = "CONFIRMED"
    challenge.auth_id = user.username
    challenge.save()

    # También actualizar transferencia vinculada
    transfer = Transfer.objects.filter(payment_id=payment_id).first()
    if transfer:
        transfer.status = "ACSC"
        transfer.auth_id = user.username
        transfer.timestamp = timezone.now()
        transfer.save()

    return {
        "paymentId": payment_id,
        "status": "ACSC",
        "timestamp": timezone.now().isoformat(),
        "auth_id": user.username
    }
