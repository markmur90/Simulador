from django.contrib import admin
from .models import (
    Debtor, DebtorAccount,
    Creditor, CreditorAccount,
    CreditorAgent, PaymentIdentification,
    ClientID, Kid, Transfer,
    LogTransferencia
)


@admin.register(Debtor)
class DebtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'customer_id')
    search_fields = ('name', 'customer_id')
    list_filter = ('address__country',)


@admin.register(DebtorAccount)
class DebtorAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'debtor', 'iban', 'currency')
    search_fields = ('debtor__name', 'iban')
    list_filter = ('currency',)


@admin.register(Creditor)
class CreditorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('address__country',)


@admin.register(CreditorAccount)
class CreditorAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'creditor', 'iban', 'currency')
    search_fields = ('creditor__name', 'iban')
    list_filter = ('currency',)


@admin.register(CreditorAgent)
class CreditorAgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'bic', 'financial_institution_id')
    search_fields = ('bic', 'financial_institution_id')


@admin.register(PaymentIdentification)
class PaymentIdentificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'end_to_end_id', 'instruction_id')
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
        'instructed_amount', 'currency',
        'requested_execution_date', 'status', 'created_at'
    )
    search_fields = (
        'payment_id', 'debtor__name', 'creditor__name'
    )
    list_filter = ('status', 'currency', 'requested_execution_date')
    date_hierarchy = 'requested_execution_date'
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)


@admin.register(LogTransferencia)
class LogTransferenciaAdmin(admin.ModelAdmin):
    list_display = ('registro', 'tipo_log', 'created_at')
    search_fields = ('registro', 'tipo_log')
    list_filter = ('tipo_log',)
    date_hierarchy = 'created_at'
