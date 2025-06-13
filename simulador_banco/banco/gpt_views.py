from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .models import (
    Debtor, DebtorAccount, Creditor, CreditorAccount,
    CreditorAgent, ClientID, Kid, Transfer
)
from .forms import (
    DebtorForm, DebtorAccountForm, CreditorForm, CreditorAccountForm,
    CreditorAgentForm, ClientIDForm, KidForm, TransferForm
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
    success_url = reverse_lazy('dashboard')


class KidCreateView(LoginRequiredMixin, generic.CreateView):
    model = Kid
    form_class = KidForm
    template_name = 'api/GPT4/create_kid.html'
    success_url = reverse_lazy('dashboard')


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