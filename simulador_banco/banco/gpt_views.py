from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
import weasyprint
from decimal import Decimal
from django.db import ProtectedError

from .models import (
    ClientID, CreditorAgent, Debtor, DebtorAccount, Creditor, CreditorAccount, Kid,
    Transfer, PaymentIdentification, AccountMovement
)
from .forms import (
    DebtorForm, DebtorAccountForm, CreditorForm, CreditorAccountForm,
    CreditorAgentForm, ClientIDForm, KidForm, TransferForm,
    DebtorUpdateForm
)
from services.transfer_services import TransferService
from services.api_validator import APITransferValidator


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

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Cuenta de débito creada exitosamente.')
            return response
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Nueva Cuenta de Débito'
        return context


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

    def form_invalid(self, form):
        """
        Maneja los errores de validación del formulario.
        Si hay errores en form.errors, los mantiene en sus campos específicos.
        """
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        """
        Intenta guardar el formulario y maneja cualquier error que ocurra.
        """
        try:
            self.object = form.save()
            messages.success(self.request, 'Transferencia creada exitosamente.')
            return redirect(self.get_success_url())
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                # Si el error tiene un diccionario de mensajes, actualizar los errores del formulario
                for field, error in e.message_dict.items():
                    form.add_error(field, error)
            else:
                # Si es un error simple, agregarlo al formulario
                form.add_error(None, str(e))
            return self.form_invalid(form)


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

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Transferencia actualizada exitosamente.')
            return response
        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


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


class SendTransferView(LoginRequiredMixin, generic.UpdateView):
    model = Transfer
    template_name = 'api/GPT4/send_transfer.html'
    fields = []  # No necesitamos campos editables
    slug_field = 'payment_id'
    slug_url_kwarg = 'payment_id'

    def get_success_url(self):
        return reverse_lazy('transfer_detailGPT4', kwargs={'payment_id': self.object.payment_id})

    def form_valid(self, form):
        try:
            # Primero validamos la transferencia para la API
            es_valido, error_msg = APITransferValidator.validate_transfer_for_api(self.object)
            
            if not es_valido:
                messages.error(self.request, f'Error de validación: {error_msg}')
                return redirect('transfer_detailGPT4', payment_id=self.object.payment_id)
            
            # Si la validación es exitosa, formateamos los datos para la API
            datos_api = APITransferValidator.format_transfer_for_api(self.object)
            
            # Intentar procesar la transferencia
            TransferService.process_transfer(self.object)
            
            messages.success(self.request, 'Transferencia validada y enviada exitosamente.')
            return super().form_valid(form)
            
        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect('transfer_detailGPT4', payment_id=self.object.payment_id)
        except Exception as e:
            messages.error(self.request, f'Error al procesar la transferencia: {str(e)}')
            return redirect('transfer_detailGPT4', payment_id=self.object.payment_id)


class DownloadTransferPDFView(LoginRequiredMixin, View):
    def get(self, request, payment_id):
        transfer = get_object_or_404(Transfer, payment_id=payment_id)
        
        # Preparar el contexto para la plantilla
        context = {
            'transfer': transfer,
            'generated_at': timezone.now()
        }
        
        # Renderizar el HTML
        html = render_to_string('api/GPT4/transfer_pdf.html', context)
        
        # Crear el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="transfer_{payment_id}.pdf"'
        
        # Generar PDF con WeasyPrint
        pdf = weasyprint.HTML(string=html).write_pdf()
        response.write(pdf)
        
        return response


class AccountStatementPDFView(LoginRequiredMixin, View):
    def get(self, request, account_id):
        account = get_object_or_404(DebtorAccount, pk=account_id)
        
        # Obtener los movimientos filtrados por fecha si se especifica
        movements = account.movimientos.order_by('-fecha')
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        
        if start_date:
            movements = movements.filter(fecha__date__gte=start_date)
        if end_date:
            movements = movements.filter(fecha__date__lte=end_date)
        
        # Preparar el contexto para la plantilla
        context = {
            'account': account,
            'movements': movements,
            'start_date': start_date,
            'end_date': end_date,
            'generated_at': timezone.now()
        }
        
        # Renderizar el HTML
        html = render_to_string('api/GPT4/account_statement_pdf.html', context)
        
        # Crear el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="account_statement_{account.iban}.pdf"'
        
        # Generar PDF con WeasyPrint
        pdf = weasyprint.HTML(string=html).write_pdf()
        response.write(pdf)
        
        return response


class DebtorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Debtor
    template_name = 'api/GPT4/debtor_detail.html'
    context_object_name = 'debtor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener las cuentas del deudor
        context['accounts'] = self.object.accounts.all()
        # Obtener las transferencias del deudor
        context['transfers'] = self.object.transfers.order_by('-created_at')[:10]
        
        # Añadir fechas para los filtros
        today = timezone.now().date()
        context['today'] = today
        context['week_ago'] = today - timedelta(days=7)
        context['month_ago'] = today - timedelta(days=30)
        
        return context


class DebtorAccountDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DebtorAccount
    template_name = 'api/GPT4/delete_debtor_account.html'
    success_url = reverse_lazy('list_debtor_accountsGPT4')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Cuenta eliminada exitosamente.')
            return response
        except ProtectedError:
            messages.error(request, 'No se puede eliminar esta cuenta porque tiene movimientos o transferencias asociadas.')
            return redirect('list_debtor_accountsGPT4')
        except Exception as e:
            messages.error(request, f'Error al eliminar la cuenta: {str(e)}')
            return redirect('list_debtor_accountsGPT4')