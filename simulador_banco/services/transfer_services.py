import random
import datetime
from typing import Any, Dict
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from banco.models import Transfer, DebtorAccount, OTPChallenge, LogTransferencia

class TransferService:
    RATE_LIMIT = 5
    WINDOW_MINUTES = 5

    @staticmethod
    @transaction.atomic
    def ingest_transfer(data: Dict[str, Any]) -> Transfer:
        payment_id = data.pop("Idempotency-Id", None) or data.get("payment_id")
        if not payment_id:
            raise ValidationError("'payment_id' requerido")
        data["payment_id"] = payment_id

        existing = Transfer.objects.filter(payment_id=payment_id).first()
        if existing:
            return existing

        window_start = timezone.now() - datetime.timedelta(minutes=TransferService.WINDOW_MINUTES)
        recent_count = Transfer.objects.filter(
            debtor_account_id=data["debtor_account_id"],
            created_at__gte=window_start
        ).count()
        if recent_count >= TransferService.RATE_LIMIT:
            return Transfer.objects.create(status='RJCT', **data)

        data["status"] = 'PDNG'
        transfer = Transfer.objects.create(**data)

        # Generar OTP
        otp = f"{random.randint(100000, 999999)}"
        OTPChallenge.objects.create(
            payment_id=payment_id,
            otp=otp,
            transfer_data=data,
            status="CREATED"
        )

        # Procesar la transferencia inmediatamente
        try:
            # Verificar fondos
            debtor_account = DebtorAccount.objects.select_for_update().get(
                id=transfer.debtor_account.id
            )
            
            if debtor_account.balance < transfer.instructed_amount:
                transfer.status = 'RJCT'
                transfer.save()
                LogTransferencia.objects.create(
                    registro=payment_id,
                    tipo_log='ERROR',
                    contenido='Fondos insuficientes'
                )
            else:
                # Realizar la transferencia
                debtor_account.balance -= transfer.instructed_amount
                debtor_account.save()
                
                transfer.status = 'ACSC'
                transfer.save()
                
                LogTransferencia.objects.create(
                    registro=payment_id,
                    tipo_log='TRANSFER',
                    contenido=f'Transferencia completada: {transfer.instructed_amount} {transfer.currency}'
                )
        except Exception as e:
            transfer.status = 'RJCT'
            transfer.save()
            LogTransferencia.objects.create(
                registro=payment_id,
                tipo_log='ERROR',
                contenido=f'Error al procesar la transferencia: {str(e)}'
            )

        return transfer

    @staticmethod
    def confirm_transfer(payment_id, otp_input, user):
        challenge = OTPChallenge.objects.get(payment_id=payment_id, otp=otp_input, status="CREATED")
        challenge.status = "CONFIRMED"
        challenge.auth_id = user.username
        challenge.save()

        transfer = Transfer.objects.filter(payment_id=payment_id).first()
        if transfer:
            transfer.status = "ACCP"
            transfer.auth_id = user.username
            transfer.save()

        return {
            "paymentId": payment_id,
            "status": "ACCP",
            "timestamp": timezone.now().isoformat(),
            "auth_id": user.username
        }
