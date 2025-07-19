from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
import uuid
from django.utils import timezone
from django.db import transaction

from .models import (
    ClientID, CreditorAgent, Debtor, DebtorAccount, Creditor, CreditorAccount, Kid,
    Transfer, AccountMovement, LogTransferencia
)
from .forms import (
    DebtorForm, DebtorAccountForm, CreditorForm, CreditorAccountForm,
    CreditorAgentForm, ClientIDForm, KidForm, TransferForm, TransferInternaForm,
    DebtorUpdateForm
)


class DebtorListView(LoginRequiredMixin, generic.ListView):
    model = Debtor
    template_name = 'api/GPT4/list_debtor.html'
    context_object_name = 'debtors'


class DebtorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Debtor
    form_class = DebtorForm
    template_name = 'api/GPT4/create_debtor.html'
    success_url = reverse_lazy('list_debtorsGPT4')


class DebtorAccountListView(LoginRequiredMixin, generic.ListView):
    model = DebtorAccount
    template_name = 'api/GPT4/list_debtor_accounts.html'
    context_object_name = 'accounts'


class DebtorAccountCreateView(LoginRequiredMixin, generic.CreateView):
    model = DebtorAccount
    form_class = DebtorAccountForm
    template_name = 'api/GPT4/create_debtor_account.html'
    success_url = reverse_lazy('list_debtor_accountsGPT4')


class CreditorListView(LoginRequiredMixin, generic.ListView):
    model = Creditor
    template_name = 'api/GPT4/list_creditors.html'
    context_object_name = 'creditors'


class CreditorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Creditor
    form_class = CreditorForm
    template_name = 'api/GPT4/create_creditor.html'
    success_url = reverse_lazy('list_creditorsGPT4')


class CreditorAccountListView(LoginRequiredMixin, generic.ListView):
    model = CreditorAccount
    template_name = 'api/GPT4/list_creditor_accounts.html'
    context_object_name = 'accounts'


class CreditorAccountCreateView(LoginRequiredMixin, generic.CreateView):
    model = CreditorAccount
    form_class = CreditorAccountForm
    template_name = 'api/GPT4/create_creditor_account.html'
    success_url = reverse_lazy('list_creditor_accountsGPT4')


class CreditorAgentListView(LoginRequiredMixin, generic.ListView):
    model = CreditorAgent
    template_name = 'api/GPT4/list_creditor_agents.html'
    context_object_name = 'agents'


class CreditorAgentCreateView(LoginRequiredMixin, generic.CreateView):
    model = CreditorAgent
    form_class = CreditorAgentForm
    template_name = 'api/GPT4/create_creditor_agent.html'
    success_url = reverse_lazy('list_creditor_agentsGPT4')


class ClientIDCreateView(LoginRequiredMixin, generic.CreateView):
    model = ClientID
    form_class = ClientIDForm
    template_name = 'api/GPT4/create_clientid.html'
    success_url = reverse_lazy('list_clientidsGPT4')


class KidCreateView(LoginRequiredMixin, generic.CreateView):
    model = Kid
    form_class = KidForm
    template_name = 'api/GPT4/create_kid.html'
    success_url = reverse_lazy('list_kidsGPT4')


class TransferListView(LoginRequiredMixin, generic.ListView):
    model = Transfer
    template_name = 'api/GPT4/list_transfer.html'
    context_object_name = 'transfers'
    paginate_by = 20


class TransferCreateView(LoginRequiredMixin, generic.CreateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'api/GPT4/create_transfer.html'
    success_url = reverse_lazy('list_transferGPT4')


class TransferDetailView(LoginRequiredMixin, generic.DetailView):
    model = Transfer
    slug_field = 'payment_id'
    slug_url_kwarg = 'payment_id'
    template_name = 'api/GPT4/transfer_detail.html'


class TransferUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Transfer
    form_class = TransferForm
    slug_field = 'payment_id'
    slug_url_kwarg = 'payment_id'
    template_name = 'api/GPT4/edit_transfer.html'
    success_url = reverse_lazy('list_transferGPT4')


class ClientIDListView(LoginRequiredMixin, generic.ListView):
    model = ClientID
    template_name = 'api/GPT4/list_clientsid.html'
    context_object_name = 'clientids'


class ClientIDUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ClientID
    form_class = ClientIDForm
    template_name = 'api/GPT4/edit_clientid.html'
    success_url = reverse_lazy('list_clientidsGPT4')
    pk_url_kwarg = 'codigo'


class ClientIDDeleteView(LoginRequiredMixin, View):
    def post(self, request, codigo):
        obj = get_object_or_404(ClientID, pk=codigo)
        obj.delete()
        return redirect('list_clientidsGPT4')


class KidListView(LoginRequiredMixin, generic.ListView):
    model = Kid
    template_name = 'api/GPT4/list_kids.html'
    context_object_name = 'kids'


class KidUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Kid
    form_class = KidForm
    template_name = 'api/GPT4/edit_kid.html'
    success_url = reverse_lazy('list_kidsGPT4')
    pk_url_kwarg = 'codigo'


class KidDeleteView(LoginRequiredMixin, View):
    def post(self, request, codigo):
        obj = get_object_or_404(Kid, pk=codigo)
        obj.delete()
        return redirect('list_kidsGPT4')


class DebtorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Debtor
    form_class = DebtorUpdateForm
    template_name = 'api/GPT4/edit_debtor.html'
    success_url = reverse_lazy('list_debtorsGPT4')


class DebtorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Debtor
    template_name = 'api/GPT4/delete_debtor.html'
    success_url = reverse_lazy('list_debtorsGPT4')


class TransferInternaCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'api/GPT4/create_transfer_interna.html'
    form_class = TransferInternaForm
    success_url = reverse_lazy('list_transferGPT4')

    def get_debtor_accounts(self, debtor_id):
        """Obtener las cuentas de un deudor específico"""
        return DebtorAccount.objects.filter(debtor_id=debtor_id)

    def form_valid(self, form):
        # Obtener los datos del formulario
        cuenta_origen = form.cleaned_data['cuenta_origen']
        cuenta_destino = form.cleaned_data['cuenta_destino']
        monto = form.cleaned_data['monto']
        concepto = form.cleaned_data['concepto']

        try:
            # Iniciar transacción para asegurar la integridad
            with transaction.atomic():
                # Crear la transferencia
                transfer = Transfer.objects.create(
                    payment_id=str(uuid.uuid4()),
                    debtor=cuenta_origen.debtor,
                    debtor_account=cuenta_origen,
                    creditor=cuenta_destino.debtor,  # Usamos el deudor destino como acreedor
                    creditor_account=cuenta_destino,  # Usamos la cuenta destino como cuenta acreedora
                    instructed_amount=monto,
                    currency=cuenta_origen.currency,
                    purpose_code='OTHR',  # Código para transferencias internas
                    requested_execution_date=timezone.now().date(),
                    remittance_information_unstructured=concepto,
                    status='ACSC'  # Completada exitosamente
                )

                # Crear movimiento de débito en cuenta origen
                AccountMovement.objects.create(
                    account=cuenta_origen,
                    tipo='PAYMENT',
                    monto=monto
                )

                # Crear movimiento de crédito en cuenta destino
                AccountMovement.objects.create(
                    account=cuenta_destino,
                    tipo='DEPOSIT',
                    monto=monto
                )

                # Registrar en el log
                LogTransferencia.objects.create(
                    registro=transfer.payment_id,
                    tipo_log='TRANSFER',
                    contenido=f'Transferencia interna exitosa de {cuenta_origen.iban} a {cuenta_destino.iban} por {monto} {cuenta_origen.currency}'
                )

        except Exception as e:
            # Si algo falla, registrar el error
            LogTransferencia.objects.create(
                registro=str(uuid.uuid4()),
                tipo_log='ERROR',
                contenido=f'Error en transferencia interna: {str(e)}'
            )
            form.add_error(None, f'Error al procesar la transferencia: {str(e)}')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Transferencia Interna'
        return context

def get_accounts_by_debtor(request):
    """Vista para obtener las cuentas de un deudor vía AJAX"""
    debtor_id = request.GET.get('debtor_id')
    if not debtor_id:
        return JsonResponse({'accounts': []})
    
    accounts = DebtorAccount.objects.filter(debtor_id=debtor_id)
    accounts_data = [{
        'id': account.id,
        'iban': account.iban,
        'balance': str(account.balance),
        'currency': account.currency
    } for account in accounts]
    
    return JsonResponse({'accounts': accounts_data})