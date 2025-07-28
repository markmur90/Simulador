import random
import datetime
import logging
from typing import Any, Dict
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from banco.models import Transfer, DebtorAccount, OTPChallenge, LogTransferencia, PaymentIdentification, AccountMovement
import uuid

logger = logging.getLogger(__name__)

class TransferService:
    RATE_LIMIT = 5
    WINDOW_MINUTES = 5

    @staticmethod
    @transaction.atomic
    def ingest_transfer(data: Dict[str, Any]) -> Transfer:
        logger.debug("Iniciando ingest_transfer")
        logger.debug(f"Datos recibidos: {data}")
        
        try:
            payment_id = data.pop("Idempotency-Id", None) or data.get("payment_id")
            if not payment_id:
                payment_id = str(uuid.uuid4())
            data["payment_id"] = payment_id
            logger.debug(f"Payment ID generado/recibido: {payment_id}")

            existing = Transfer.objects.filter(payment_id=payment_id).first()
            if existing:
                logger.debug(f"Transferencia existente encontrada con payment_id: {payment_id}")
                return existing

            window_start = timezone.now() - datetime.timedelta(minutes=TransferService.WINDOW_MINUTES)
            recent_count = Transfer.objects.filter(
                debtor_account_id=data["debtor_account_id"],
                created_at__gte=window_start
            ).count()
            logger.debug(f"Transferencias recientes para la cuenta: {recent_count}")
            
            if recent_count >= TransferService.RATE_LIMIT:
                logger.debug(f"Límite de transferencias excedido para la cuenta")
                data["status"] = 'RJCT'
                return Transfer.objects.create(**data)

            # Crear PaymentIdentification con UUIDs válidos
            logger.debug("Creando PaymentIdentification")
            payment_identification = PaymentIdentification.objects.create(
                end_to_end_id=uuid.uuid4(),
                instruction_id=uuid.uuid4()
            )
            data["payment_identification"] = payment_identification
            data["status"] = 'PDNG'
            logger.debug(f"PaymentIdentification creado: {payment_identification.instruction_id}")

            # Crear la transferencia
            logger.debug("Creando transferencia")
            transfer = Transfer.objects.create(**data)
            logger.debug(f"Transferencia creada con ID: {transfer.id}")

            # Generar OTP
            logger.debug("Generando OTP")
            otp = f"{random.randint(100000, 999999)}"
            otp_challenge = OTPChallenge.objects.create(
                payment_id=payment_id,
                otp=otp,
                status="CREATED"
            )
            logger.debug(f"OTP generado: {otp_challenge.otp}")

            # Registrar en el log
            logger.debug("Registrando log de la transferencia")
            LogTransferencia.objects.create(
                registro=payment_id,
                tipo_log='CREATED',
                contenido=f'Transferencia creada: {transfer.instructed_amount} {transfer.currency}'
            )

            return transfer

        except Exception as e:
            import traceback
            logger.error("Error en ingest_transfer:")
            logger.error(f"Tipo de error: {type(e).__name__}")
            logger.error(f"Mensaje de error: {str(e)}")
            logger.error("Traceback completo:")
            logger.error(traceback.format_exc())
            
            # Registrar el error en el log
            LogTransferencia.objects.create(
                registro=str(uuid.uuid4()),
                tipo_log='ERROR',
                contenido=f'Error en ingest_transfer: {str(e)}\n{traceback.format_exc()}'
            )
            
            raise ValidationError(f"Error al procesar la transferencia: {str(e)}")

    @staticmethod
    @transaction.atomic
    def process_transfer(transfer: Transfer) -> Transfer:
        """Procesa una transferencia existente."""
        try:
            # Verificar fondos
            debtor_account = DebtorAccount.objects.select_for_update().get(
                id=transfer.debtor_account.id
            )
            
            # Validar fondos suficientes
            if debtor_account.balance < transfer.instructed_amount:
                transfer.status = 'RJCT'
                transfer.save()
                LogTransferencia.objects.create(
                    registro=transfer.payment_id,
                    tipo_log='ERROR',
                    contenido='Fondos insuficientes'
                )
                return transfer

            # Validar monedas compatibles
            if debtor_account.currency != transfer.currency:
                transfer.status = 'RJCT'
                transfer.save()
                LogTransferencia.objects.create(
                    registro=transfer.payment_id,
                    tipo_log='ERROR',
                    contenido='Moneda incompatible'
                )
                return transfer

            # Crear movimiento de débito (esto actualizará el saldo automáticamente)
            AccountMovement.objects.create(
                account=debtor_account,
                tipo=AccountMovement.PAYMENT,
                monto=transfer.instructed_amount
            )

            # Si es una transferencia interna, buscar la cuenta deudora correspondiente
            creditor_account = transfer.creditor_account
            if creditor_account:
                try:
                    # Buscar la cuenta deudora correspondiente por IBAN
                    destino_account = DebtorAccount.objects.select_for_update().get(
                        iban=creditor_account.iban
                    )
                    # Crear movimiento de crédito (esto actualizará el saldo automáticamente)
                    AccountMovement.objects.create(
                        account=destino_account,
                        tipo=AccountMovement.DEPOSIT,
                        monto=transfer.instructed_amount
                    )
                except DebtorAccount.DoesNotExist:
                    logger.warning(f"No se encontró cuenta deudora para el IBAN: {creditor_account.iban}")

            transfer.status = 'ACSC'
            transfer.save()
            
            LogTransferencia.objects.create(
                registro=transfer.payment_id,
                tipo_log='TRANSFER',
                contenido=f'Transferencia completada: {transfer.instructed_amount} {transfer.currency}'
            )

        except Exception as e:
            logger.error(f"Error al procesar transferencia {transfer.payment_id}: {str(e)}")
            logger.error(traceback.format_exc())
            
            transfer.status = 'RJCT'
            transfer.save()
            LogTransferencia.objects.create(
                registro=transfer.payment_id,
                tipo_log='ERROR',
                contenido=f'Error al procesar la transferencia: {str(e)}'
            )

        return transfer

    @staticmethod
    def confirm_transfer(payment_id: str, otp_input: str, user: Any) -> Dict[str, Any]:
        """Confirma una transferencia con OTP."""
        with transaction.atomic():
            challenge = OTPChallenge.objects.select_for_update().get(
                payment_id=payment_id, 
                otp=otp_input, 
                status="CREATED"
            )
            challenge.status = "CONFIRMED"
            challenge.auth_id = user.username
            challenge.save()

            transfer = Transfer.objects.select_for_update().get(payment_id=payment_id)
            transfer.status = "ACCP"
            transfer.auth_id = user.username
            transfer.save()

            # Procesar la transferencia
            transfer = TransferService.process_transfer(transfer)

            return {
                "paymentId": payment_id,
                "status": transfer.status,
                "timestamp": timezone.now().isoformat(),
                "auth_id": user.username
            }
