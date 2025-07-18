#!/usr/bin/env python
import os
import sys
import django
import logging
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simulador_banco.settings')
django.setup()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

from banco.models import (
    Debtor, DebtorAccount, Creditor, CreditorAccount,
    Transfer, AccountMovement
)
from banco.services.security_services import TelegramService
from services.transfer_services import TransferService
import pyotp

def setup_test_data():
    """Crea datos de prueba."""
    try:
        # Crear deudores
        debtor1 = Debtor.objects.create(
            name="Alice Test",
            customer_id="TEST001",
            totp_secret=pyotp.random_base32()
        )
        debtor2 = Debtor.objects.create(
            name="Bob Test",
            customer_id="TEST002",
            totp_secret=pyotp.random_base32()
        )
        
        # Crear cuentas de deudores
        account1 = DebtorAccount.objects.create(
            debtor=debtor1,
            iban="ES1234567890123456789012",
            currency="EUR",
            balance=Decimal("1000.00")
        )
        account2 = DebtorAccount.objects.create(
            debtor=debtor2,
            iban="ES9876543210987654321098",
            currency="EUR",
            balance=Decimal("500.00")
        )
        
        # Crear acreedor
        creditor = Creditor.objects.create(
            name="Shop Test",
            identification="SHOP001"
        )
        creditor_account = CreditorAccount.objects.create(
            creditor=creditor,
            iban="ES5555555555555555555555",
            currency="EUR"
        )
        
        return {
            'debtor1': debtor1,
            'debtor2': debtor2,
            'account1': account1,
            'account2': account2,
            'creditor': creditor,
            'creditor_account': creditor_account
        }
        
    except Exception as e:
        logger.error(f"Error creando datos de prueba: {str(e)}")
        raise

def test_internal_transfer(data):
    """Prueba una transferencia interna entre deudores."""
    try:
        logger.info("Iniciando prueba de transferencia interna...")
        
        # Realizar transferencia
        transfer = TransferService.create_internal_transfer(
            origin_account=data['account1'],
            destination_account=data['account2'],
            amount=Decimal("100.00"),
            description="Prueba de transferencia interna"
        )
        
        logger.info(f"Transferencia creada con ID: {transfer.payment_id}")
        
        # Verificar saldos
        data['account1'].refresh_from_db()
        data['account2'].refresh_from_db()
        
        assert data['account1'].balance == Decimal("900.00")
        assert data['account2'].balance == Decimal("600.00")
        
        logger.info("Prueba de transferencia interna exitosa")
        return transfer
        
    except Exception as e:
        logger.error(f"Error en prueba de transferencia interna: {str(e)}")
        raise

def test_external_transfer(data):
    """Prueba una transferencia a un acreedor con validación OTP."""
    try:
        logger.info("Iniciando prueba de transferencia externa...")
        
        # Crear transferencia
        transfer = TransferService.create_external_transfer(
            origin_account=data['account1'],
            destination_account=data['creditor_account'],
            amount=Decimal("50.00"),
            description="Prueba de transferencia externa"
        )
        
        logger.info(f"Transferencia externa creada con ID: {transfer.payment_id}")
        
        # Generar y validar OTP
        totp = pyotp.TOTP(data['debtor1'].totp_secret)
        otp = totp.now()
        
        logger.info(f"Validando OTP: {otp}")
        is_valid = TransferService.validate_otp(transfer.payment_id, otp)
        
        assert is_valid, "OTP debería ser válido"
        
        # Verificar saldo
        data['account1'].refresh_from_db()
        assert data['account1'].balance == Decimal("850.00")
        
        logger.info("Prueba de transferencia externa exitosa")
        return transfer
        
    except Exception as e:
        logger.error(f"Error en prueba de transferencia externa: {str(e)}")
        raise

def cleanup_test_data(data):
    """Limpia los datos de prueba."""
    try:
        logger.info("Limpiando datos de prueba...")
        
        # Eliminar en orden para evitar errores de FK
        AccountMovement.objects.filter(
            account__in=[data['account1'], data['account2']]
        ).delete()
        Transfer.objects.all().delete()
        DebtorAccount.objects.all().delete()
        CreditorAccount.objects.all().delete()
        Debtor.objects.all().delete()
        Creditor.objects.all().delete()
        
        logger.info("Datos de prueba eliminados")
        
    except Exception as e:
        logger.error(f"Error limpiando datos de prueba: {str(e)}")
        raise

def main():
    """Ejecuta todas las pruebas."""
    try:
        # Crear datos de prueba
        logger.info("Iniciando pruebas...")
        data = setup_test_data()
        
        # Probar transferencia interna
        internal_transfer = test_internal_transfer(data)
        
        # Probar transferencia externa con OTP
        external_transfer = test_external_transfer(data)
        
        # Verificar estados
        status1 = TransferService.get_transfer_status(internal_transfer.payment_id)
        status2 = TransferService.get_transfer_status(external_transfer.payment_id)
        
        logger.info(f"Estado transferencia interna: {status1['status']}")
        logger.info(f"Estado transferencia externa: {status2['status']}")
        
        # Limpiar datos
        cleanup_test_data(data)
        
        logger.info("Todas las pruebas completadas exitosamente")
        
    except Exception as e:
        logger.error(f"Error en pruebas: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 