from django.db import transaction
from banco.models import (
    PostalAddress, Debtor, DebtorAccount, Creditor, CreditorAccount,
    CreditorAgent, Transfer, AccountMovement
)
from decimal import Decimal

def create_test_data():
    with transaction.atomic():
        # Crear agente acreedor
        creditor_agent = CreditorAgent.objects.create(
            bic='BSCHESMMXXX',
            financial_institution_id='BANCO_SANTANDER',
            other_information='Banco Santander'
        )

        # Crear direcciones
        addr_debtor1 = PostalAddress.objects.create(
            country='ES',
            street='Calle Mayor 1',
            city='Madrid'
        )

        addr_debtor2 = PostalAddress.objects.create(
            country='ES',
            street='Calle Gran Vía 2',
            city='Madrid'
        )

        addr_creditor = PostalAddress.objects.create(
            country='ES',
            street='Avenida Diagonal 123',
            city='Barcelona'
        )

        # Crear deudores
        debtor1 = Debtor.objects.create(
            name='Juan Pérez',
            customer_id='CUST001',
            address=addr_debtor1
        )

        debtor2 = Debtor.objects.create(
            name='María García',
            customer_id='CUST002',
            address=addr_debtor2
        )

        # Crear acreedor
        creditor = Creditor.objects.create(
            name='Empresa ABC',
            address=addr_creditor
        )

        # Crear cuentas de deudores
        debtor1_account = DebtorAccount.objects.create(
            debtor=debtor1,
            iban='ES9121000418450200051332',
            currency='EUR',
            balance=Decimal('10000.00')
        )

        debtor2_account = DebtorAccount.objects.create(
            debtor=debtor2,
            iban='ES7100750327630600000173',
            currency='EUR',
            balance=Decimal('15000.00')
        )

        # Crear cuenta de acreedor
        creditor_account = CreditorAccount.objects.create(
            creditor=creditor,
            iban='ES8401826294169201629461',
            currency='EUR'
        )

        # Crear movimientos iniciales para las cuentas de deudores
        AccountMovement.objects.create(
            account=debtor1_account,
            tipo='DEPOSIT',
            monto=Decimal('10000.00')
        )

        AccountMovement.objects.create(
            account=debtor2_account,
            tipo='DEPOSIT',
            monto=Decimal('15000.00')
        )

        print("Datos de prueba creados exitosamente:")
        print(f"Deudor 1: {debtor1.name} (ID: {debtor1.id})")
        print(f"Cuenta Deudor 1: {debtor1_account.iban}")
        print(f"Deudor 2: {debtor2.name} (ID: {debtor2.id})")
        print(f"Cuenta Deudor 2: {debtor2_account.iban}")
        print(f"Acreedor: {creditor.name} (ID: {creditor.id})")
        print(f"Cuenta Acreedor: {creditor_account.iban}")
        print(f"Agente Acreedor: {creditor_agent.bic}")

if __name__ == '__main__':
    create_test_data() 