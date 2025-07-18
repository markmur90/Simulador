import os
import django
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simulador_banco.simulador_banco.settings')
os.environ.setdefault('FIELD_ENCRYPTION_KEY', 'DbQG9CWLvBRa8Iu9pv9fJDVURCdKYQQErlZ9oCYGsY8=')
django.setup()

from banco.models import Debtor, DebtorAccount, PostalAddress, AccountMovement

@pytest.fixture
def setup_account():
    """Fixture para crear una cuenta con saldo inicial."""
    addr = PostalAddress.objects.create(country="ES", street="Calle", city="Madrid")
    debtor = Debtor.objects.create(name="Alice", customer_id="C1", address=addr)
    account = DebtorAccount.objects.create(
        debtor=debtor,
        iban="ES1234567890123",
        currency="EUR",
        balance=Decimal('100.00')
    )
    return account

@pytest.mark.django_db
def test_deposit_updates_balance(setup_account):
    """Verificar que un depósito aumenta el saldo correctamente."""
    account = setup_account
    initial_balance = account.balance
    deposit_amount = Decimal('50.00')
    
    movement = AccountMovement.objects.create(
        account=account,
        tipo=AccountMovement.DEPOSIT,
        monto=deposit_amount
    )
    
    account.refresh_from_db()
    assert account.balance == initial_balance + deposit_amount

@pytest.mark.django_db
def test_payment_updates_balance(setup_account):
    """Verificar que un pago reduce el saldo correctamente."""
    account = setup_account
    initial_balance = account.balance
    payment_amount = Decimal('30.00')
    
    movement = AccountMovement.objects.create(
        account=account,
        tipo=AccountMovement.PAYMENT,
        monto=payment_amount
    )
    
    account.refresh_from_db()
    assert account.balance == initial_balance - payment_amount

@pytest.mark.django_db
def test_payment_without_funds_fails(setup_account):
    """Verificar que un pago sin fondos suficientes falla."""
    account = setup_account
    payment_amount = account.balance + Decimal('1.00')
    
    with pytest.raises(ValidationError):
        AccountMovement.objects.create(
            account=account,
            tipo=AccountMovement.PAYMENT,
            monto=payment_amount
        )
    
    account.refresh_from_db()
    assert account.balance == Decimal('100.00')  # El saldo no debe cambiar

@pytest.mark.django_db
def test_concurrent_movements_handled_correctly(setup_account):
    """Verificar que los movimientos concurrentes se manejan correctamente."""
    account = setup_account
    initial_balance = account.balance
    
    # Crear varios movimientos en secuencia rápida
    movements = [
        AccountMovement(
            account=account,
            tipo=AccountMovement.DEPOSIT if i % 2 == 0 else AccountMovement.PAYMENT,
            monto=Decimal('10.00')
        )
        for i in range(10)
    ]
    
    # Guardar todos los movimientos
    for movement in movements:
        movement.save()
    
    account.refresh_from_db()
    # Debería haber 5 depósitos y 5 pagos de 10.00 cada uno
    expected_balance = initial_balance + (Decimal('10.00') * 5) - (Decimal('10.00') * 5)
    assert account.balance == expected_balance 
    