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
        # Crear o actualizar superusuario
        try:
            superuser = User.objects.get(username='markmur88')
            superuser.set_password('Ptf8454Jd55')
            superuser.is_superuser = True
            superuser.is_staff = True
            superuser.save()
            self.stdout.write(self.style.SUCCESS('Superusuario actualizado'))
        except User.DoesNotExist:
            superuser = User.objects.create_superuser(
                username='markmur88',
                password='Ptf8454Jd55',
                email='admin@example.com'
            )
            self.stdout.write(self.style.SUCCESS('Superusuario creado'))

        # Limpiar datos existentes
        PostalAddress.objects.all().delete()
        Debtor.objects.all().delete()
        DebtorAccount.objects.all().delete()
        Creditor.objects.all().delete()
        CreditorAccount.objects.all().delete()
        CreditorAgent.objects.all().delete()

        # Crear direcciones
        dir_debtor1 = PostalAddress.objects.create(
            country='ES',
            street='Calle Deudor 123',
            city='Madrid'
        )
        
        dir_debtor2 = PostalAddress.objects.create(
            country='ES',
            street='Avenida Principal 456',
            city='Barcelona'
        )
        
        dir_creditor_santander = PostalAddress.objects.create(
            country='ES',
            street='Paseo de Pereda 9-12',
            city='Santander'
        )

        # Crear primer deudor
        debtor1 = Debtor.objects.create(
            name='Juan Pérez',
            customer_id='CUST001',
            address=dir_debtor1
        )

        # Crear segundo deudor
        debtor2 = Debtor.objects.create(
            name='María López',
            customer_id='CUST002',
            address=dir_debtor2
        )

        # Crear cuentas deudoras
        debtor_account1 = DebtorAccount.objects.create(
            debtor=debtor1,
            iban='ES9121000418450200051332',
            currency='EUR',
            balance=Decimal('10000.00')
        )

        debtor_account2 = DebtorAccount.objects.create(
            debtor=debtor2,
            iban='ES7721000418450200051333',
            currency='EUR',
            balance=Decimal('15000.00')
        )

        # Crear acreedor Santander
        creditor_santander = Creditor.objects.create(
            name='Banco Santander S.A.',
            address=dir_creditor_santander
        )

        # Crear cuenta acreedora Santander
        creditor_account_santander = CreditorAccount.objects.create(
            creditor=creditor_santander,
            iban='ES2100491500051234567892',
            currency='EUR',
            balance=Decimal('1000000.00')
        )

        # Crear agente financiero Santander
        CreditorAgent.objects.create(
            bic='BSCHESMMXXX',
            financial_institution_id='BSCH',
            other_information='Banco Santander'
        )

        # Crear o actualizar oficial bancario
        try:
            oficial = OficialBancario.objects.get(username='403069k1')
            oficial.set_password('bar1588623')
            oficial.save()
            self.stdout.write(self.style.SUCCESS('Oficial bancario actualizado'))
        except OficialBancario.DoesNotExist:
            oficial = OficialBancario.objects.create(
                username='403069k1'
            )
            oficial.set_password('bar1588623')
            oficial.save()
            self.stdout.write(self.style.SUCCESS('Oficial bancario creado'))

        self.stdout.write(self.style.SUCCESS('Datos de prueba creados exitosamente')) 