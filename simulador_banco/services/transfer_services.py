import random
import datetime
from decimal import Decimal
from typing import Dict, Optional, Tuple
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
import uuid
import secrets
import logging
import pyotp
from banco.models import (
    Transfer, Debtor, Creditor, DebtorAccount,
    CreditorAccount, CreditorAgent, PaymentIdentification,
    LogTransferencia, AccountMovement
)
from banco.services.security_services import TelegramService

logger = logging.getLogger('banco.transfers')

class TransferService:
    """Servicio para gestionar transferencias bancarias."""

    @classmethod
    @transaction.atomic
    def create_internal_transfer(cls, origin_account: DebtorAccount, 
                               destination_account: DebtorAccount,
                               amount: Decimal,
                               description: str = None) -> Transfer:
        """
        Crea y procesa una transferencia entre cuentas de deudores.
        
        Args:
            origin_account: Cuenta de origen
            destination_account: Cuenta de destino
            amount: Monto a transferir
            description: Descripción opcional
            
        Returns:
            Transfer: Transferencia creada y procesada
            
        Raises:
            ValidationError: Si hay errores de validación
        """
        try:
            # Validaciones básicas
            if origin_account.id == destination_account.id:
                raise ValidationError("No se puede transferir a la misma cuenta")
                
            if origin_account.currency != destination_account.currency:
                raise ValidationError("Las monedas deben coincidir")
                
            if amount <= 0:
                raise ValidationError("El monto debe ser mayor a 0")
                
            # Validar saldo con lock
            origin_account = DebtorAccount.objects.select_for_update().get(pk=origin_account.pk)
            if origin_account.balance < amount:
                raise ValidationError("Saldo insuficiente")
                
            # Crear identificadores
            payment_id = str(uuid.uuid4())
            payment_identification = PaymentIdentification.objects.create(
                end_to_end_id=str(uuid.uuid4()),
                instruction_id=str(uuid.uuid4())
            )
            
            # Crear transferencia
            transfer = Transfer.objects.create(
                payment_id=payment_id,
                debtor=origin_account.debtor,
                creditor=destination_account.debtor,
                debtor_account=origin_account,
                creditor_account=None,  # No se usa para transferencias internas
                creditor_agent=CreditorAgent.objects.first(),
                instructed_amount=amount,
                currency=origin_account.currency,
                purpose_code='GDSV',
                requested_execution_date=timezone.now().date(),
                payment_identification=payment_identification,
                remittance_information_unstructured=description,
                status='PDNG'
            )
            
            # Crear movimientos
            AccountMovement.objects.create(
                account=origin_account,
                tipo='PAYMENT',
                monto=amount,
                descripcion=f'Transferencia a {destination_account.debtor.name} - {description or ""}'.strip()
            )
            
            AccountMovement.objects.create(
                account=destination_account,
                tipo='DEPOSIT',
                monto=amount,
                descripcion=f'Transferencia de {origin_account.debtor.name} - {description or ""}'.strip()
            )
            
            # Actualizar estado
            transfer.status = 'ACCP'
            transfer.save()
            
            # Registrar en log
            logger.info(
                f"Transferencia interna exitosa - ID: {payment_id} - "
                f"De: {origin_account.debtor.name} - "
                f"A: {destination_account.debtor.name} - "
                f"Monto: {amount} {origin_account.currency}"
            )
            
            # Crear imagen y notificar por Telegram
            image_path = TelegramService.create_transfer_image(transfer)
            TelegramService.send_notification(
                f"Nueva transferencia interna procesada:\n"
                f"De: {origin_account.debtor.name}\n"
                f"A: {destination_account.debtor.name}\n"
                f"Monto: {amount} {origin_account.currency}\n"
                f"Estado: {transfer.status}",
                image_path
            )
            
            return transfer
            
        except Exception as e:
            logger.error(f"Error en transferencia interna: {str(e)}")
            raise

    @classmethod
    @transaction.atomic
    def create_external_transfer(cls, origin_account: DebtorAccount,
                               destination_account: CreditorAccount,
                               amount: Decimal,
                               description: str = None) -> Transfer:
        """
        Crea una transferencia a una cuenta de acreedor.
        
        Args:
            origin_account: Cuenta de origen
            destination_account: Cuenta de destino (acreedor)
            amount: Monto a transferir
            description: Descripción opcional
            
        Returns:
            Transfer: Transferencia creada
            
        Raises:
            ValidationError: Si hay errores de validación
        """
        try:
            # Validaciones
            if origin_account.currency != destination_account.currency:
                raise ValidationError("Las monedas deben coincidir")
                
            if amount <= 0:
                raise ValidationError("El monto debe ser mayor a 0")
                
            # Validar saldo con lock
            origin_account = DebtorAccount.objects.select_for_update().get(pk=origin_account.pk)
            if origin_account.balance < amount:
                raise ValidationError("Saldo insuficiente")
                
            # Crear identificadores
            payment_id = str(uuid.uuid4())
            payment_identification = PaymentIdentification.objects.create(
                end_to_end_id=str(uuid.uuid4()),
                instruction_id=str(uuid.uuid4())
            )
            
            # Crear transferencia
            transfer = Transfer.objects.create(
                payment_id=payment_id,
                debtor=origin_account.debtor,
                creditor=destination_account.creditor,
                debtor_account=origin_account,
                creditor_account=destination_account,
                creditor_agent=CreditorAgent.objects.first(),
                instructed_amount=amount,
                currency=origin_account.currency,
                purpose_code='GDSV',
                requested_execution_date=timezone.now().date(),
                payment_identification=payment_identification,
                remittance_information_unstructured=description,
                status='PDNG'
            )
            
            # Crear movimiento de salida
            AccountMovement.objects.create(
                account=origin_account,
                tipo='PAYMENT',
                monto=amount,
                descripcion=f'Transferencia a {destination_account.creditor.name} - {description or ""}'.strip()
            )
            
            # Registrar en log
            logger.info(
                f"Transferencia externa creada - ID: {payment_id} - "
                f"De: {origin_account.debtor.name} - "
                f"A: {destination_account.creditor.name} - "
                f"Monto: {amount} {origin_account.currency}"
            )
            
            # Crear imagen y notificar por Telegram
            image_path = TelegramService.create_transfer_image(transfer)
            TelegramService.send_notification(
                f"Nueva transferencia externa pendiente:\n"
                f"De: {origin_account.debtor.name}\n"
                f"A: {destination_account.creditor.name}\n"
                f"Monto: {amount} {origin_account.currency}\n"
                f"Estado: {transfer.status}",
                image_path
            )
            
            return transfer
            
        except Exception as e:
            logger.error(f"Error en transferencia externa: {str(e)}")
            raise

    @classmethod
    def get_transfer_status(cls, payment_id: str) -> Dict:
        """
        Obtiene el estado actual de una transferencia.
        
        Args:
            payment_id: ID de la transferencia
            
        Returns:
            Dict con el estado actual
        """
        try:
            transfer = Transfer.objects.select_related(
                'debtor', 'creditor', 'debtor_account', 'creditor_account'
            ).get(payment_id=payment_id)
            
            status_info = {
                'payment_id': transfer.payment_id,
                'status': transfer.status,
                'amount': str(transfer.instructed_amount),
                'currency': transfer.currency,
                'debtor': transfer.debtor.name,
                'creditor': transfer.creditor.name,
                'created_at': transfer.created_at.isoformat(),
                'updated_at': transfer.updated_at.isoformat()
            }
            
            logger.info(f"Consultado estado de transferencia - ID: {payment_id} - Estado: {transfer.status}")
            
            return status_info
            
        except Transfer.DoesNotExist:
            logger.warning(f"Transferencia no encontrada - ID: {payment_id}")
            raise ValidationError(f"Transferencia {payment_id} no encontrada")
            
        except Exception as e:
            logger.error(f"Error consultando estado de transferencia - ID: {payment_id} - Error: {str(e)}")
            raise

    @classmethod
    def validate_otp(cls, payment_id: str, otp: str) -> bool:
        """
        Valida un código OTP para una transferencia.
        
        Args:
            payment_id: ID de la transferencia
            otp: Código OTP a validar
            
        Returns:
            bool: True si el OTP es válido
        """
        try:
            transfer = Transfer.objects.get(payment_id=payment_id)
            
            # Validar OTP usando pyotp
            totp = pyotp.TOTP(transfer.debtor.totp_secret)
            is_valid = totp.verify(otp)
            
            if is_valid:
                logger.info(f"OTP válido para transferencia - ID: {payment_id}")
                TelegramService.send_notification(
                    f"🔑 OTP validado correctamente para transferencia {payment_id}"
                )
            else:
                logger.warning(f"OTP inválido para transferencia - ID: {payment_id}")
                TelegramService.send_notification(
                    f"❌ Intento de OTP inválido para transferencia {payment_id}"
                )
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Error validando OTP - ID: {payment_id} - Error: {str(e)}")
            raise
