from django.core.management.base import BaseCommand
from django.utils import timezone
from banco.models import (
    Debtor,
    DebtorAccount,
    Creditor,
    CreditorAccount,
    CreditorAgent,
    Transfer,
    PaymentIdentification
)
import uuid
from decimal import Decimal

class Command(BaseCommand):
    help = 'Simula transferencias internas y externas'

    def handle(self, *args, **options):
        # Obtener cuentas
        debtor_account = DebtorAccount.objects.get(iban='ES9121000418450200051332')
        creditor_account_interno = CreditorAccount.objects.get(iban='ES7921000813610123456789')
        creditor_account_externo = CreditorAccount.objects.get(iban='DE89370400440532013000')
        creditor_agent = CreditorAgent.objects.first()

        # Crear transferencia interna
        payment_id_interno = str(uuid.uuid4())
        payment_identification_interno = PaymentIdentification.objects.create(
            end_to_end_id=f'E2E-{payment_id_interno[:8]}',
            instruction_id=f'INST-{payment_id_interno[:8]}'
        )

        transfer_interno = Transfer.objects.create(
            payment_id=payment_id_interno,
            debtor=debtor_account.debtor,
            creditor=creditor_account_interno.creditor,
            debtor_account=debtor_account,
            creditor_account=creditor_account_interno,
            creditor_agent=creditor_agent,
            instructed_amount=Decimal('100.00'),
            currency='EUR',
            purpose_code='GDSV',
            requested_execution_date=timezone.now().date(),
            remittance_information_unstructured='Transferencia interna de prueba',
            status='ACSC',
            payment_identification=payment_identification_interno
        )

        # Crear transferencia externa
        payment_id_externo = str(uuid.uuid4())
        payment_identification_externo = PaymentIdentification.objects.create(
            end_to_end_id=f'E2E-{payment_id_externo[:8]}',
            instruction_id=f'INST-{payment_id_externo[:8]}'
        )

        transfer_externo = Transfer.objects.create(
            payment_id=payment_id_externo,
            debtor=debtor_account.debtor,
            creditor=creditor_account_externo.creditor,
            debtor_account=debtor_account,
            creditor_account=creditor_account_externo,
            creditor_agent=creditor_agent,
            instructed_amount=Decimal('200.00'),
            currency='EUR',
            purpose_code='GDSV',
            requested_execution_date=timezone.now().date(),
            remittance_information_unstructured='Transferencia externa de prueba',
            status='ACSC',
            payment_identification=payment_identification_externo
        )

        self.stdout.write(self.style.SUCCESS(f'''
Transferencias creadas exitosamente:

1. Transferencia Interna:
   - ID: {payment_id_interno}
   - De: {debtor_account.debtor.name} ({debtor_account.iban})
   - Para: {creditor_account_interno.creditor.name} ({creditor_account_interno.iban})
   - Monto: €100.00
   - Estado: Completada

2. Transferencia Externa:
   - ID: {payment_id_externo}
   - De: {debtor_account.debtor.name} ({debtor_account.iban})
   - Para: {creditor_account_externo.creditor.name} ({creditor_account_externo.iban})
   - Monto: €200.00
   - Estado: Completada
''')) 