import pytest
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
    