from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from banco.models import (
    PostalAddress, Debtor, DebtorAccount,
    Creditor, CreditorAccount, CreditorAgent,
    PaymentIdentification
)
from decimal import Decimal

class Command(BaseCommand):
    help = 'Configura datos de prueba para el simulador bancario'

    def handle(self, *args, **options):
        # Crear direcciones
        address1 = PostalAddress.objects.create(
            country='ES',
            street='Calle Test 1',
            city='Madrid'
        )
        address2 = PostalAddress.objects.create(
            country='ES',
            street='Calle Test 2',
            city='Barcelona'
        )
        address3 = PostalAddress.objects.create(
            country='ES',
            street='Calle Test 3',
            city='Valencia'
        )

        # Crear deudores
        debtor1 = Debtor.objects.create(
            name='Deudor Test 1',
            customer_id='CUST001',
            address=address1
        )
        debtor2 = Debtor.objects.create(
            name='Deudor Test 2',
            customer_id='CUST002',
            address=address2
        )

        # Crear cuentas de deudores
        DebtorAccount.objects.create(
            debtor=debtor1,
            iban='ES9121000418450200051332',
            currency='EUR',
            balance=Decimal('10000.00')
        )
        DebtorAccount.objects.create(
            debtor=debtor2,
            iban='ES7100815465740123456789',
            currency='EUR',
            balance=Decimal('5000.00')
        )

        # Crear acreedor y su cuenta para transferencias externas
        creditor = Creditor.objects.create(
            name='Acreedor Test',
            address=address3
        )
        CreditorAccount.objects.create(
            creditor=creditor,
            iban='ES8401825699600123456789',
            currency='EUR'
        )
        CreditorAgent.objects.create(
            bic='TESTESMMXXX',
            financial_institution_id='TEST123456'
        )

        # Crear superusuario si no existe
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@test.com', 'admin123') 