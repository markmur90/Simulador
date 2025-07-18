import random
import datetime
from decimal import Decimal
from typing import Dict, Optional, Tuple
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
import uuid
import secrets

from banco.models import (
    Transfer, Debtor, Creditor, DebtorAccount,
    CreditorAccount, CreditorAgent, PaymentIdentification,
    LogTransferencia, AccountMovement
)

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
        LogTransferencia.objects.create(
            registro=payment_id,
            tipo_log='TRANSFER',
            contenido=f'Transferencia interna procesada exitosamente'
        )
        
        return transfer

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
        LogTransferencia.objects.create(
            registro=payment_id,
            tipo_log='TRANSFER',
            contenido=f'Transferencia externa creada'
        )
        
        return transfer

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
            
            return {
                'payment_id': transfer.payment_id,
                'status': transfer.status,
                'amount': str(transfer.instructed_amount),
                'currency': transfer.currency,
                'debtor': transfer.debtor.name,
                'creditor': transfer.creditor.name,
                'created_at': transfer.created_at.isoformat(),
                'updated_at': transfer.updated_at.isoformat()
            }
        except Transfer.DoesNotExist:
            raise ValidationError(f"Transferencia {payment_id} no encontrada")
