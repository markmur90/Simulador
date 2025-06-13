from django.contrib import admin
from .models import (
    OficialBancario, OTPChallenge,
    DebtorSimulado, CreditorSimulado, TransferenciaSimulada,
    Debtor, DebtorAccount,
    Creditor, CreditorAccount,
    CreditorAgent, PaymentIdentification,
    ClientID, Kid, Transfer,
    LogTransferencia, PostalAddress,
)

# ——————————————————————————————————————————————
# Inlines para embebidos
# ——————————————————————————————————————————————

class PostalAddressInline(admin.StackedInline):
    model = PostalAddress
    extra = 1            # Muestra un formulario vacío si no hay ninguno
    max_num = 1
    can_delete = True    # Permite eliminar si se creó por error


class DebtorAccountInline(admin.TabularInline):
    model = DebtorAccount
    extra = 1            # Permite crear cuentas nuevas
    fields = ('iban', 'balance', 'currency')
    readonly_fields = ('balance',)


class CreditorAccountInline(admin.TabularInline):
    model = CreditorAccount
    extra = 1            # Permite crear cuentas nuevas
    fields = ('iban', 'currency')


# ——————————————————————————————————————————————
# Admin para Banca Simulada
# ——————————————————————————————————————————————

@admin.register(OficialBancario)
class OficialBancarioAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)
    exclude = ('password_hash',)


@admin.register(OTPChallenge)
class OTPChallengeAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'challenge_id', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment_id', 'challenge_id')
    readonly_fields = ('challenge_id', 'created_at')


@admin.register(DebtorSimulado)
class DebtorSimuladoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(CreditorSimulado)
class CreditorSimuladoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(TransferenciaSimulada)
class TransferenciaSimuladaAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'debtor', 'creditor', 'monto', 'oficial', 'status_display')
    list_filter = ('oficial',)
    search_fields = ('payment_id', 'debtor__nombre', 'creditor__nombre')

    @admin.display(description='Destino / Oficial')
    def status_display(self, obj):
        return f"{obj.destino}" if obj.oficial else '—'


# ——————————————————————————————————————————————
# Admin para Banca Real
# ——————————————————————————————————————————————

@admin.register(Debtor)
class DebtorAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer_id')
    search_fields = ('name', 'customer_id')
    inlines = (PostalAddressInline, DebtorAccountInline)


@admin.register(DebtorAccount)
class DebtorAccountAdmin(admin.ModelAdmin):
    list_display = ('iban', 'debtor', 'balance', 'currency')
    search_fields = ('iban', 'debtor__name')
    list_filter = ('currency',)


@admin.register(Creditor)
class CreditorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (PostalAddressInline, CreditorAccountInline)


@admin.register(CreditorAccount)
class CreditorAccountAdmin(admin.ModelAdmin):
    list_display = ('iban', 'creditor', 'currency')
    search_fields = ('iban', 'creditor__name')
    list_filter = ('currency',)


@admin.register(CreditorAgent)
class CreditorAgentAdmin(admin.ModelAdmin):
    list_display = ('bic', 'financial_institution_id', 'other_information')
    search_fields = ('bic', 'financial_institution_id')


@admin.register(PaymentIdentification)
class PaymentIdentificationAdmin(admin.ModelAdmin):
    list_display = ('end_to_end_id', 'instruction_id')
    search_fields = ('end_to_end_id', 'instruction_id')


@admin.register(ClientID)
class ClientIDAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'client_id')
    search_fields = ('codigo', 'client_id')


@admin.register(Kid)
class KidAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'kid')
    search_fields = ('codigo', 'kid')


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = (
        'payment_id', 'debtor', 'creditor',
        'instructed_amount', 'currency', 'status', 'requested_execution_date'
    )
    search_fields = (
        'payment_id',
        'debtor__name', 'creditor__name',
        'payment_identification__end_to_end_id'
    )
    list_filter = ('status', 'currency', 'requested_execution_date')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': (
                'payment_id', 'status',
                'requested_execution_date', 'instructed_amount',
                'currency',
            )
        }),
        ('Partes', {
            'fields': (
                'debtor', 'debtor_account',
                'creditor', 'creditor_account',
                'creditor_agent',
            )
        }),
        ('Identificadores', {
            'fields': ('payment_identification', 'client', 'kid', 'auth_id')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(LogTransferencia)
class LogTransferenciaAdmin(admin.ModelAdmin):
    list_display = ('tipo_log', 'registro', 'created_at')
    search_fields = ('registro', 'contenido')
    list_filter = ('tipo_log', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(PostalAddress)
class PostalAddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street')
    search_fields = ('country', 'city', 'street')