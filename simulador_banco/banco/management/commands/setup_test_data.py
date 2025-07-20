from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from banco.models import (
    PostalAddress,
    Debtor,
    DebtorAccount,
    Creditor,
    CreditorAccount,
    CreditorAgent,
    OficialBancario
)
from decimal import Decimal

class Command(BaseCommand):
    help = 'Configura datos de prueba para el simulador bancario'

    def handle(self, *args, **options):
        # Crear direcciones
        dir_debtor = PostalAddress.objects.create(
            country='ES',
            street='Calle Deudor 123',
            city='Madrid'
        )
        
        dir_creditor_interno = PostalAddress.objects.create(
            country='ES',
            street='Calle Acreedor Interno 456',
            city='Barcelona'
        )
        
        dir_creditor_externo = PostalAddress.objects.create(
            country='DE',
            street='External Bank Street 789',
            city='Berlin'
        )

        # Crear deudor
        debtor = Debtor.objects.create(
            name='Juan Pérez',
            customer_id='CUST001',
            address=dir_debtor
        )

        # Crear cuenta deudora
        debtor_account = DebtorAccount.objects.create(
            debtor=debtor,
            iban='ES9121000418450200051332',
            currency='EUR',
            balance=Decimal('10000.00')
        )

        # Crear acreedor interno
        creditor_interno = Creditor.objects.create(
            name='Ana García',
            address=dir_creditor_interno
        )

        # Crear cuenta acreedora interna
        creditor_account_interno = CreditorAccount.objects.create(
            creditor=creditor_interno,
            iban='ES7921000813610123456789',
            currency='EUR',
            balance=Decimal('5000.00')
        )

        # Crear acreedor externo
        creditor_externo = Creditor.objects.create(
            name='Deutsche Bank AG',
            address=dir_creditor_externo
        )

        # Crear cuenta acreedora externa
        creditor_account_externo = CreditorAccount.objects.create(
            creditor=creditor_externo,
            iban='DE89370400440532013000',
            currency='EUR',
            balance=Decimal('100000.00')
        )

        # Crear agente financiero
        CreditorAgent.objects.create(
            bic='DEUTDEFF',
            financial_institution_id='DEUTDE',
            other_information='Deutsche Bank'
        )

        # Crear oficial bancario
        oficial = OficialBancario.objects.create(
            username='oficial1'
        )
        oficial.set_password('password123')
        oficial.save()

        self.stdout.write(self.style.SUCCESS('Datos de prueba creados exitosamente')) 