import pytest
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simulador_banco.simulador_banco.settings')
os.environ.setdefault('FIELD_ENCRYPTION_KEY', 'DbQG9CWLvBRa8Iu9pv9fJDVURCdKYQQErlZ9oCYGsY8=')
django.setup()
from simulador_banco.banco.models import (
    DebtorSimulado,
    CreditorSimulado,
    TransferenciaSimulada,
)

@pytest.mark.django_db
def test_transferencia_creacion():
    d = DebtorSimulado.objects.create(nombre="Alice")
    c = CreditorSimulado.objects.create(nombre="Bob")
    t = TransferenciaSimulada.objects.create(
        payment_id="PID123",
        debtor=d,
        creditor=c,
        monto=100
    )
    assert TransferenciaSimulada.objects.filter(pk=t.pk).exists()
    