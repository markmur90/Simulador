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
    LogTransferencia, AccountMovement
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
        # Log para depuración inicial
        LogTransferencia.objects.create(
            registro=f"DEBUG_VALIDATE_{debtor_account[:8]}",
            tipo_log='DEBUG',
            contenido=f'Iniciando validación de cuentas - Deudor: {debtor_account}, Acreedor: {creditor_account}'
        )
        
        # Normalizar IBANs
        debtor_account = ''.join(debtor_account.split()).upper()
        creditor_account = ''.join(creditor_account.split()).upper()
        
        # Log después de normalización
        LogTransferencia.objects.create(
            registro=f"DEBUG_VALIDATE_{debtor_account[:8]}",
            tipo_log='DEBUG',
            contenido=f'IBANs normalizados - Deudor: {debtor_account}, Acreedor: {creditor_account}'
        )
        
        # Buscar cuenta deudora
        try:
            debit_acc = DebtorAccount.objects.select_related('debtor').get(iban=debtor_account)
        except DebtorAccount.DoesNotExist:
            LogTransferencia.objects.create(
                registro=f"DEBUG_VALIDATE_{debtor_account[:8]}",
                tipo_log='ERROR',
                contenido=f'Cuenta de débito no encontrada para IBAN: {debtor_account}'
            )
            raise ValidationError({
                'debtor_account': 'Cuenta de débito no encontrada'
            })
        
        # Log de éxito para cuenta deudora
        LogTransferencia.objects.create(
            registro=f"DEBUG_VALIDATE_{debtor_account[:8]}",
            tipo_log='DEBUG',
            contenido=f'Cuenta de débito encontrada: {debit_acc.iban}'
        )
        
        # Buscar cuenta acreedora
        try:
            # Primero intentar encontrar como cuenta interna
            try:
                credit_acc = DebtorAccount.objects.select_related('debtor').get(iban=creditor_account)
                is_internal = True
            except DebtorAccount.DoesNotExist:
                # Si no es interna, buscar como cuenta externa
                credit_acc = CreditorAccount.objects.select_related('creditor').get(iban=creditor_account)
                is_internal = False
        except (DebtorAccount.DoesNotExist, CreditorAccount.DoesNotExist):
            LogTransferencia.objects.create(
                registro=f"DEBUG_VALIDATE_{debtor_account[:8]}",
                tipo_log='ERROR',
                contenido=f'Cuenta de crédito no encontrada para IBAN: {creditor_account}'
            )
            raise ValidationError({
                'creditor_account': 'Cuenta de crédito no encontrada'
            })

        # Validar que el deudor tenga todos los datos necesarios
        if not debit_acc.debtor.name or not debit_acc.debtor.address:
            raise ValidationError({
                'debtor_account': 'Datos incompletos del deudor'
            })

        # Validar que el acreedor tenga todos los datos necesarios
        if is_internal:
            if not credit_acc.debtor.name or not credit_acc.debtor.address:
                raise ValidationError({
                    'creditor_account': 'Datos incompletos del deudor destino'
                })
        else:
            if not credit_acc.creditor.name or not credit_acc.creditor.address:
                raise ValidationError({
                    'creditor_account': 'Datos incompletos del acreedor'
                })

        return debit_acc, credit_acc

    @classmethod
    def validate_balance(cls, account: DebtorAccount, amount: Decimal) -> None:
        """Valida que la cuenta tenga saldo suficiente."""
        if account.balance < amount:
            raise ValidationError({
                'instructed_amount': 'Saldo insuficiente'
            })

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

        # Determinar si es transferencia interna
        is_internal = isinstance(transfer.creditor_account, DebtorAccount)

        # Actualizar saldos
        with transaction.atomic():
            # Descontar de la cuenta origen
            transfer.debtor_account.balance -= transfer.instructed_amount
            transfer.debtor_account.save()

            # Registrar movimiento de salida
            AccountMovement.objects.create(
                account=transfer.debtor_account,
                tipo='TRANSFER_OUT',
                monto=transfer.instructed_amount,
                descripcion=f'Transferencia enviada a {transfer.creditor.name} - ID: {transfer.payment_id}'
            )

            if is_internal:
                # Para transferencias internas, actualizar la cuenta destino
                creditor_account = transfer.creditor_account
                creditor_account.balance += transfer.instructed_amount
                creditor_account.save()

                # Registrar movimiento de entrada
                AccountMovement.objects.create(
                    account=creditor_account,
                    tipo='TRANSFER_IN',
                    monto=transfer.instructed_amount,
                    descripcion=f'Transferencia recibida de {transfer.debtor.name} - ID: {transfer.payment_id}'
                )

                # Actualizar estado a completado
                transfer.status = 'ACSC'
            else:
                # Para transferencias externas, iniciar proceso con API externa
                try:
                    # Aquí iría la lógica de comunicación con la API externa
                    # Por ahora solo simulamos el proceso
                    transfer.status = 'ACCP'
                except Exception as e:
                    # Si falla la API externa, revertir la transferencia
                    transfer.debtor_account.balance += transfer.instructed_amount
                    transfer.debtor_account.save()
                    transfer.status = 'RJCT'
                    raise ValidationError(f'Error al procesar transferencia externa: {str(e)}')

            transfer.save()

            # Registrar en el log
            LogTransferencia.objects.create(
                registro=transfer.payment_id,
                tipo_log='PROCESS',
                contenido=f'Transferencia procesada: {transfer.status}'
            )

    @classmethod
    def get_transfer_status(cls, payment_id: str) -> dict:
        """
        Obtiene el estado actual de una transferencia.
        
        Args:
            payment_id: ID único de la transferencia
            
        Returns:
            dict: Información del estado de la transferencia
        """
        try:
            transfer = Transfer.objects.get(payment_id=payment_id)
            return {
                'payment_id': transfer.payment_id,
                'status': transfer.status,
                'amount': str(transfer.instructed_amount),
                'currency': transfer.currency,
                'created_at': transfer.created_at.isoformat(),
                'updated_at': transfer.updated_at.isoformat()
            }
        except Transfer.DoesNotExist:
            raise ValidationError('Transferencia no encontrada')
