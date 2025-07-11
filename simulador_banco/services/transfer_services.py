import random
import datetime
from decimal import Decimal
from typing import Dict, Optional
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
import uuid
import secrets

from banco.models import (
    Transfer, Debtor, Creditor, DebtorAccount,
    CreditorAccount, CreditorAgent, PaymentIdentification,
    LogTransferencia
)

class TransferService:
    REQUIRED_FIELDS = [
        'payment_id', 'debtor_account', 'creditor_account',
        'instructed_amount', 'currency'
    ]

    @classmethod
    def validate_transfer_data(cls, data: Dict) -> None:
        """Valida los datos de la transferencia."""
        # Validar campos requeridos
        missing = [f for f in cls.REQUIRED_FIELDS if f not in data]
        if missing:
            raise ValidationError(f'Campos requeridos faltantes: {", ".join(missing)}')

        # Validar montos
        amount = data.get('instructed_amount')
        if not amount or Decimal(str(amount)) <= 0:
            raise ValidationError('El monto debe ser mayor a 0')

    @classmethod
    def validate_accounts(cls, debtor_account: str, creditor_account: str) -> tuple:
        """Valida y retorna las cuentas de débito y crédito."""
        try:
            debit_acc = DebtorAccount.objects.select_related('debtor').get(
                iban=debtor_account
            )
        except DebtorAccount.DoesNotExist:
            raise ValidationError('Cuenta de débito no encontrada')

        try:
            credit_acc = CreditorAccount.objects.select_related('creditor').get(
                iban=creditor_account
            )
        except CreditorAccount.DoesNotExist:
            raise ValidationError('Cuenta de crédito no encontrada')

        # Validar que el deudor tenga todos los datos necesarios
        if not debit_acc.debtor.name or not debit_acc.debtor.address:
            raise ValidationError('Datos incompletos del deudor')

        # Validar que el acreedor tenga todos los datos necesarios
        if not credit_acc.creditor.name or not credit_acc.creditor.address:
            raise ValidationError('Datos incompletos del acreedor')

        return debit_acc, credit_acc

    @classmethod
    def validate_balance(cls, account: DebtorAccount, amount: Decimal) -> None:
        """Valida que la cuenta tenga saldo suficiente."""
        if account.balance < amount:
            raise ValidationError('Saldo insuficiente')

    @classmethod
    def generate_auth_id(cls) -> str:
        """Genera un ID de autorización único."""
        return f"AUTH_{secrets.token_hex(8).upper()}"

    @classmethod
    @transaction.atomic
    def create_transfer(cls, data: Dict) -> Transfer:
        """
        Crea una nueva transferencia.
        
        Args:
            data: Diccionario con los datos de la transferencia
            
        Returns:
            Transfer: Objeto de transferencia creado
            
        Raises:
            ValidationError: Si los datos son inválidos
        """
        # Validar datos básicos
        cls.validate_transfer_data(data)

        # Validar y obtener cuentas
        debit_acc, credit_acc = cls.validate_accounts(
            data['debtor_account'],
            data['creditor_account']
        )

        # Validar saldo
        amount = Decimal(str(data['instructed_amount']))
        cls.validate_balance(debit_acc, amount)

        # Crear identificación de pago
        payment_id = PaymentIdentification.objects.create(
            end_to_end_id=data.get('end_to_end_id', uuid.uuid4().hex),
            instruction_id=data.get('instruction_id', uuid.uuid4().hex)
        )

        # Crear transferencia
        transfer = Transfer.objects.create(
            payment_id=data['payment_id'],
            debtor=debit_acc.debtor,
            creditor=credit_acc.creditor,
            debtor_account=debit_acc,
            creditor_account=credit_acc,
            creditor_agent=data.get('creditor_agent'),
            instructed_amount=amount,
            currency=data.get('currency', 'EUR'),
            purpose_code=data.get('purpose_code', 'GDSV'),
            requested_execution_date=data.get('requested_execution_date', timezone.now().date()),
            remittance_information_unstructured=data.get('remittance_information_unstructured'),
            payment_identification=payment_id,
            status='PDNG'
        )

        LogTransferencia.objects.create(
            registro=transfer.payment_id,
            tipo_log='TRANSFER',
            contenido=f'Transferencia creada: {transfer.payment_id}'
        )

        return transfer

    @classmethod
    @transaction.atomic
    def process_transfer(cls, transfer: Transfer) -> None:
        """
        Procesa una transferencia existente.
        
        Args:
            transfer: Objeto de transferencia a procesar
        """
        # Validar estado
        if transfer.status not in ['PDNG', 'ACWP']:
            raise ValidationError(f'Estado inválido para procesar: {transfer.status}')

        # Validar saldo nuevamente
        cls.validate_balance(transfer.debtor_account, transfer.instructed_amount)

        # Actualizar saldos
        transfer.debtor_account.balance -= transfer.instructed_amount
        transfer.debtor_account.save()

        # Actualizar estado
        transfer.status = 'ACCP'
        
        # Generar auth_id solo cuando se acepta la transferencia
        if not transfer.auth_id:
            transfer.auth_id = cls.generate_auth_id()
            
        transfer.save()

        LogTransferencia.objects.create(
            registro=transfer.payment_id,
            tipo_log='TRANSFER',
            contenido=f'Transferencia procesada: {transfer.payment_id} - Auth ID: {transfer.auth_id}'
        )

    @classmethod
    def get_transfer_info(cls, payment_id: str) -> Dict:
        """
        Obtiene información detallada de una transferencia.
        
        Args:
            payment_id: ID de la transferencia
            
        Returns:
            Dict: Información de la transferencia
            
        Raises:
            ValidationError: Si la transferencia no existe
        """
        try:
            transfer = Transfer.objects.select_related(
                'debtor', 'creditor',
                'debtor_account', 'creditor_account',
                'creditor_agent', 'payment_identification'
            ).get(payment_id=payment_id)
        except Transfer.DoesNotExist:
            raise ValidationError('Transferencia no encontrada')

        return {
            'payment_id': transfer.payment_id,
            'status': transfer.status,
            'auth_id': transfer.auth_id,
            'amount': float(transfer.instructed_amount),
            'currency': transfer.currency,
            'debtor': {
                'name': transfer.debtor.name,
                'account': transfer.debtor_account.iban
            },
            'creditor': {
                'name': transfer.creditor.name,
                'account': transfer.creditor_account.iban
            },
            'created_at': transfer.created_at.isoformat(),
            'updated_at': transfer.updated_at.isoformat()
        }
