import datetime
import random
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
     - generación automática de OTP
    """
    RATE_LIMIT = 5
    WINDOW_MINUTES = 5

    @staticmethod
    @transaction.atomic
    def ingest_transfer(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inserta o rechaza una transferencia según reglas y genera un OTP.
        Retorna estructura con estado y OTP generado.
        """

        payment_id = data.pop("Idempotency-Id", None) or data.get("payment_id")
        if not payment_id:
            raise ValidationError("'payment_id' requerido")
        data["payment_id"] = payment_id

        # Idempotencia
        existing = Transfer.objects.filter(payment_id=payment_id).first()
        if existing:
            return {
                "transfer_id": existing.id,
                "payment_id": existing.payment_id,
                "status": existing.status,
                "otp": None  # Ya fue creado previamente
            }

        # Rate-limit
        window_start = timezone.now() - datetime.timedelta(
            minutes=TransferService.WINDOW_MINUTES
        )
        recent_count = Transfer.objects.filter(
            debtor_account_id=data["debtor_account_id"],
            created_at__gte=window_start
        ).count()
        if recent_count >= TransferService.RATE_LIMIT:
            transfer = Transfer.objects.create(status='RJCT', **data)
            return {
                "transfer_id": transfer.id,
                "payment_id": transfer.payment_id,
                "status": transfer.status,
                "otp": None
            }

        # Crear transferencia
        data["status"] = 'PDNG'
        transfer = Transfer.objects.create(**data)

        # Generar OTP
        otp = f"{random.randint(100000, 999999)}"

        # Registrar OTPChallenge
        OTPChallenge.objects.create(
            payment_id=payment_id,
            otp=otp,
            transfer_data=data,
            status="CREATED"
        )

        # Programar ejecución futura
        process_transfer_task.apply_async(
            args=[transfer.id],
            countdown=TransferService.WINDOW_MINUTES * 60
        )

        return {
            "transfer_id": transfer.id,
            "payment_id": transfer.payment_id,
            "status": transfer.status,
            "otp": otp
        }


def confirm_transfer(payment_id, otp_input, user):
    challenge = OTPChallenge.objects.get(payment_id=payment_id, otp=otp_input, status="CREATED")
    challenge.status = "CONFIRMED"
    challenge.auth_id = user.username
    challenge.save()

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
