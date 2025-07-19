from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse
from django.db import transaction
import uuid
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from django.utils import timezone

from .models import (
    ClientID, CreditorAgent, Debtor, DebtorAccount, Creditor, CreditorAccount, Kid,
    Transfer, AccountMovement
)
from .forms import (
    DebtorForm, DebtorAccountForm, CreditorForm, CreditorAccountForm,
    CreditorAgentForm, ClientIDForm, KidForm, TransferForm, TransferFormGPT4,
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


class TransferCreateViewGPT4(LoginRequiredMixin, generic.CreateView):
    model = Transfer
    form_class = TransferFormGPT4
    template_name = 'api/GPT4/create_transfer_gpt4.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['debtors'] = Debtor.objects.all()
        # Añadir el tipo de transferencia al contexto
        context['tipo'] = self.request.GET.get('tipo', '')
        return context

    def get_initial(self):
        initial = super().get_initial()
        # Establecer el tipo de transferencia inicial basado en el parámetro de la URL
        tipo = self.request.GET.get('tipo')
        if tipo in ['INTERNAL', 'EXTERNAL']:
            initial['transaction_type'] = tipo
        return initial

    def form_valid(self, form):
        with transaction.atomic():
            transfer = form.save(commit=False)
            
            # Generar payment_id único
            transfer.payment_id = str(uuid.uuid4())
            
            # Si es transferencia interna, actualizar saldos
            if transfer.transaction_type == 'INTERNAL':
                debtor_account = transfer.debtor_account
                creditor_account = transfer.internal_creditor_account
                amount = transfer.instructed_amount

                # Verificar saldo suficiente
                if debtor_account.balance < amount:
                    form.add_error(None, 'Saldo insuficiente en la cuenta de origen')
                    return self.form_invalid(form)

                # Crear movimientos de cuenta
                AccountMovement.objects.create(
                    account=debtor_account,
                    tipo='PAYMENT',
                    monto=amount
                )
                AccountMovement.objects.create(
                    account=creditor_account,
                    tipo='DEPOSIT',
                    monto=amount
                )

                # Actualizar saldos
                debtor_account.balance -= amount
                creditor_account.balance += amount
                debtor_account.save()
                creditor_account.save()

                # Marcar como completada
                transfer.status = 'ACCC'
            else:
                # Para transferencias externas, mantener el flujo normal
                transfer.status = 'PDNG'

            transfer.save()
            
            # Redirigir a la vista de envío para transferencias externas
            if transfer.transaction_type == 'EXTERNAL':
                return redirect('send_transfer_viewGPT4', payment_id=transfer.payment_id)
            else:
                # Para transferencias internas, ir directamente al detalle
                return redirect('transfer_detailGPT4', payment_id=transfer.payment_id)

def get_debtor_accounts(request):
    debtor_id = request.GET.get('debtor_id')
    accounts = DebtorAccount.objects.filter(debtor_id=debtor_id).values('id', 'iban', 'balance')
    return JsonResponse({'accounts': list(accounts)})

class TransferListViewGPT4(LoginRequiredMixin, generic.ListView):
    model = Transfer
    template_name = 'api/GPT4/list_transfer_gpt4.html'
    context_object_name = 'transfers'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        transaction_type = self.request.GET.get('tipo')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        return queryset.order_by('-created_at')

class TransferDetailViewGPT4(LoginRequiredMixin, generic.DetailView):
    model = Transfer
    template_name = 'api/GPT4/transfer_detail_gpt4.html'
    slug_field = 'payment_id'
    slug_url_kwarg = 'payment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transfer = self.get_object()
        if transfer.transaction_type == 'INTERNAL':
            context['movements'] = AccountMovement.objects.filter(
                account__in=[transfer.debtor_account, transfer.internal_creditor_account],
                fecha__gte=transfer.created_at
            ).order_by('fecha')
        return context

class TransferSendViewGPT4(LoginRequiredMixin, View):
    template_name = 'api/GPT4/send_transfer.html'

    def get(self, request, payment_id):
        transfer = get_object_or_404(Transfer, payment_id=payment_id)
        return render(request, self.template_name, {'transfer': transfer})

    def post(self, request, payment_id):
        transfer = get_object_or_404(Transfer, payment_id=payment_id)
        
        if transfer.transaction_type == 'INTERNAL':
            # Las transferencias internas ya están procesadas
            return redirect('transfer_detailGPT4', payment_id=payment_id)
        
        try:
            # Aquí iría la lógica de envío de transferencia externa
            # transfer_service = TransferService() # This line was commented out in the original file
            # result = transfer_service.send_transfer(transfer) # This line was commented out in the original file
            
            # if result.get('status') == 'success': # This line was commented out in the original file
            #     transfer.status = 'ACSP'  # En proceso # This line was commented out in the original file
            #     transfer.save() # This line was commented out in the original file
            #     messages.success(request, 'Transferencia enviada correctamente') # This line was commented out in the original file
            #     return redirect('transfer_detailGPT4', payment_id=payment_id) # This line was commented out in the original file
            # else: # This line was commented out in the original file
            #     messages.error(request, 'Error al enviar la transferencia: ' + result.get('message', 'Error desconocido')) # This line was commented out in the original file
                
        except Exception as e:
            # messages.error(request, f'Error al procesar la transferencia: {str(e)}') # This line was commented out in the original file
            pass # This line was commented out in the original file
        
        return render(request, self.template_name, {'transfer': transfer})

def descargar_pdfGPT4(request, payment_id):
    """Genera un PDF con los detalles de la transferencia."""
    # Obtener la transferencia
    transfer = get_object_or_404(Transfer, payment_id=payment_id)
    
    # Crear el buffer de memoria para el PDF
    buffer = BytesIO()
    
    # Crear el PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Detalle de Transferencia")
    
    # Subtítulo con el tipo de transferencia
    p.setFont("Helvetica-Bold", 12)
    tipo = "Interna" if transfer.transaction_type == 'INTERNAL' else "Externa"
    p.drawString(50, height - 80, f"Transferencia {tipo}")
    
    # Información de la transferencia
    p.setFont("Helvetica", 12)
    y = height - 120
    
    # Detalles comunes
    details = [
        ("Payment ID:", transfer.payment_id),
        ("Estado:", transfer.get_status_display()),
        ("Deudor:", transfer.debtor.name),
        ("Cuenta Deudor:", transfer.debtor_account.iban),
    ]
    
    # Detalles específicos según el tipo de transferencia
    if transfer.transaction_type == 'INTERNAL':
        details.extend([
            ("Beneficiario:", transfer.internal_creditor.name if transfer.internal_creditor else "N/A"),
            ("Cuenta Beneficiario:", transfer.internal_creditor_account.iban if transfer.internal_creditor_account else "N/A"),
        ])
    else:
        details.extend([
            ("Acreedor:", transfer.creditor.name if transfer.creditor else "N/A"),
            ("Cuenta Acreedor:", transfer.creditor_account.iban if transfer.creditor_account else "N/A"),
            ("Agente Acreedor:", transfer.creditor_agent.bic if transfer.creditor_agent else "N/A"),
        ])
    
    # Resto de detalles comunes
    details.extend([
        ("Importe:", f"{transfer.instructed_amount} {transfer.currency}"),
        ("Fecha de Ejecución:", transfer.requested_execution_date.strftime("%d/%m/%Y")),
        ("Referencia:", transfer.remittance_information_unstructured or "N/A"),
        ("Creado:", transfer.created_at.strftime("%d/%m/%Y %H:%M")),
        ("Código de Propósito:", transfer.purpose_code),
    ])
    
    # Dibujar los detalles
    for label, value in details:
        p.drawString(50, y, f"{label} {value}")
        y -= 25
    
    # Agregar pie de página
    p.setFont("Helvetica-Italic", 8)
    p.drawString(50, 50, f"Generado el {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Finalizar el PDF
    p.showPage()
    p.save()
    
    # Preparar el archivo para descarga
    buffer.seek(0)
    filename = f"transferencia_{transfer.payment_id}_{timezone.now().strftime('%Y%m%d_%H%M')}.pdf"
    
    return FileResponse(buffer, as_attachment=True, filename=filename)