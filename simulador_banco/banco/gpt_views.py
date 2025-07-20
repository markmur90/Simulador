from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
import uuid
from django.utils import timezone
from django.db import transaction
from django.contrib import messages

from .models import (
    ClientID, CreditorAgent, Debtor, DebtorAccount, Creditor, CreditorAccount, Kid,
    Transfer, AccountMovement, LogTransferencia, PaymentIdentification, PostalAddress
)
from .forms import (
    DebtorForm, DebtorAccountForm, CreditorForm, CreditorAccountForm,
    CreditorAgentForm, ClientIDForm, KidForm, TransferForm, TransferInternaForm,
    DebtorUpdateForm
)

from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO


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
    
    def get_success_url(self):
        return reverse_lazy('transfer_detailGPT4', kwargs={'payment_id': self.object.payment_id})


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
    
    def get_success_url(self):
        return reverse_lazy('transfer_detailGPT4', kwargs={'payment_id': self.object.payment_id})

    def get_debtor_accounts(self, debtor_id):
        """Obtener las cuentas de un deudor específico"""
        return DebtorAccount.objects.filter(debtor_id=debtor_id)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Obtener los datos del formulario
                cuenta_origen = form.cleaned_data['cuenta_origen']
                cuenta_destino = form.cleaned_data['cuenta_destino']
                monto = form.cleaned_data['monto']
                concepto = form.cleaned_data['concepto']
                deudor_destino = cuenta_destino.debtor

                # Validar que las cuentas sean diferentes
                if cuenta_origen == cuenta_destino:
                    if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'error': 'No se puede transferir a la misma cuenta'
                        }, status=400)
                    form.add_error(None, 'No se puede transferir a la misma cuenta')
                    return self.form_invalid(form)

                # Validar saldo suficiente
                if cuenta_origen.balance < monto:
                    if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'error': 'Saldo insuficiente en la cuenta origen'
                        }, status=400)
                    form.add_error(None, 'Saldo insuficiente en la cuenta origen')
                    return self.form_invalid(form)

                # Generar payment_id
                payment_id = str(uuid.uuid4())
                
                # Crear PaymentIdentification
                payment_identification = PaymentIdentification.objects.create(
                    end_to_end_id=f'E2E-{payment_id[:8]}',
                    instruction_id=f'INST-{payment_id[:8]}'
                )

                # Crear o obtener un Creditor basado en el Debtor destino
                creditor, created = Creditor.objects.get_or_create(
                    name=deudor_destino.name,
                    defaults={
                        'address': PostalAddress.objects.create(
                            country=deudor_destino.address.country,
                            street=deudor_destino.address.street,
                            city=deudor_destino.address.city
                        )
                    }
                )

                # Crear o obtener CreditorAccount basada en la DebtorAccount destino
                creditor_account, created = CreditorAccount.objects.get_or_create(
                    creditor=creditor,
                    iban=cuenta_destino.iban,
                    defaults={
                        'currency': cuenta_destino.currency
                    }
                )

                # Crear o obtener CreditorAgent para transferencias internas
                creditor_agent, created = CreditorAgent.objects.get_or_create(
                    bic='INTERNALBIC',
                    defaults={
                        'financial_institution_id': 'INTERNAL001',
                        'other_information': 'Agente para transferencias internas'
                    }
                )
                
                # Crear la transferencia
                self.object = Transfer.objects.create(
                    payment_id=payment_id,
                    debtor=cuenta_origen.debtor,
                    debtor_account=cuenta_origen,
                    creditor=creditor,  # Usamos el creditor creado
                    creditor_account=creditor_account,  # Usamos la cuenta creditor creada
                    creditor_agent=creditor_agent,  # Agregamos el agente financiero interno
                    instructed_amount=monto,
                    currency=cuenta_origen.currency,
                    purpose_code='OTHR',  # Código para transferencias internas
                    requested_execution_date=timezone.now().date(),
                    remittance_information_unstructured=concepto,
                    status='ACSC',  # Completada exitosamente
                    payment_identification=payment_identification
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
                    registro=self.object.payment_id,
                    tipo_log='TRANSFER',
                    contenido=f'Transferencia interna exitosa de {cuenta_origen.iban} a {cuenta_destino.iban} por {monto} {cuenta_origen.currency}'
                )

                if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'payment_id': self.object.payment_id,
                        'message': 'Transferencia realizada con éxito'
                    })

                return super().form_valid(form)

        except Exception as e:
            # Si algo falla, registrar el error
            error_id = str(uuid.uuid4())
            LogTransferencia.objects.create(
                registro=error_id,
                tipo_log='ERROR',
                contenido=f'Error en transferencia interna: {str(e)}'
            )
            
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': f'Error al procesar la transferencia: {str(e)}'
                }, status=500)
            
            form.add_error(None, f'Error al procesar la transferencia: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'Datos de formulario inválidos',
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Transferencia Interna'
        return context

def get_accounts_by_debtor(request):
    """Vista para obtener las cuentas de un deudor vía AJAX"""
    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator

    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Debe iniciar sesión para acceder a esta funcionalidad',
            'accounts': []
        }, status=401)

    debtor_id = request.GET.get('debtor_id')
    if not debtor_id:
        return JsonResponse({
            'error': 'ID de deudor no proporcionado',
            'accounts': []
        }, status=400)
    
    try:
        # Verificar si el deudor existe
        debtor = Debtor.objects.filter(id=debtor_id).first()
        if not debtor:
            return JsonResponse({
                'error': 'Deudor no encontrado',
                'accounts': []
            }, status=404)

        # Obtener las cuentas
        accounts = DebtorAccount.objects.filter(debtor_id=debtor_id)
        
        if not accounts.exists():
            return JsonResponse({
                'message': 'El deudor no tiene cuentas asociadas',
                'accounts': []
            })

        accounts_data = [{
            'id': account.id,
            'iban': account.iban,
            'balance': str(account.balance),
            'currency': account.currency
        } for account in accounts]
        
        return JsonResponse({
            'message': 'Cuentas obtenidas exitosamente',
            'accounts': accounts_data
        })

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("Error en get_accounts_by_debtor:", error_details)  # Para debugging
        return JsonResponse({
            'error': 'Error al obtener las cuentas. Por favor, contacte al administrador.',
            'accounts': []
        }, status=500)

def get_accounts_by_creditor(request):
    """Vista para obtener las cuentas de un acreedor vía AJAX"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Debe iniciar sesión para acceder a esta funcionalidad',
            'accounts': []
        }, status=401)

    creditor_id = request.GET.get('creditor_id')
    if not creditor_id:
        return JsonResponse({
            'error': 'ID de acreedor no proporcionado',
            'accounts': []
        }, status=400)
    
    try:
        # Verificar si el acreedor existe
        creditor = Creditor.objects.filter(id=creditor_id).first()
        if not creditor:
            return JsonResponse({
                'error': 'Acreedor no encontrado',
                'accounts': []
            }, status=404)

        # Obtener las cuentas
        accounts = CreditorAccount.objects.filter(creditor_id=creditor_id)
        
        if not accounts.exists():
            return JsonResponse({
                'message': 'El acreedor no tiene cuentas asociadas',
                'accounts': []
            })

        accounts_data = [{
            'id': account.id,
            'iban': account.iban,
            'currency': account.currency
        } for account in accounts]
        
        return JsonResponse({
            'message': 'Cuentas obtenidas exitosamente',
            'accounts': accounts_data
        })

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("Error en get_accounts_by_creditor:", error_details)
        return JsonResponse({
            'error': 'Error al obtener las cuentas. Por favor, contacte al administrador.',
            'accounts': []
        }, status=500)

@login_required
def descargar_pdf_gpt4(request, payment_id):
    """Vista para descargar el PDF de una transferencia."""
    try:
        transfer = Transfer.objects.get(payment_id=payment_id)
        
        # Crear el PDF usando ReportLab
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        
        # Título
        elements.append(Paragraph("Comprobante de Transferencia", title_style))
        elements.append(Spacer(1, 20))
        
        # Datos de la transferencia
        data = [
            ["ID de Pago", transfer.payment_id],
            ["Estado", transfer.get_status_display()],
            ["Fecha", transfer.created_at.strftime("%d/%m/%Y %H:%M:%S")],
            ["Monto", f"{transfer.instructed_amount} {transfer.currency}"],
            ["Cuenta Origen", transfer.debtor_account.iban],
            ["Titular Origen", transfer.debtor.name],
            ["Cuenta Destino", transfer.creditor_account.iban],
            ["Titular Destino", transfer.creditor.name],
            ["Concepto", transfer.remittance_information_unstructured or ""],
        ]
        
        # Crear tabla
        table = Table(data, colWidths=[150, 350])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(table)
        
        # Generar PDF
        doc.build(elements)
        
        # Obtener el valor del PDF del buffer y crear la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        
        # Crear la respuesta HTTP con el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="transferencia_{payment_id}.pdf"'
        response.write(pdf)
        
        return response
        
    except Transfer.DoesNotExist:
        return HttpResponse("Transferencia no encontrada", status=404)
    except Exception as e:
        return HttpResponse(f"Error al generar PDF: {str(e)}", status=500)

@login_required
def send_transfer_view_gpt4(request, payment_id):
    """Vista para enviar una transferencia."""
    transfer = get_object_or_404(Transfer, payment_id=payment_id)
    
    try:
        # Registrar el intento de envío
        LogTransferencia.objects.create(
            registro=transfer.payment_id,
            tipo_log='TRANSFER',
            contenido=f'Iniciando envío de transferencia {transfer.payment_id}'
        )
        
        # Actualizar estado
        transfer.status = 'ACSP'  # En proceso
        transfer.save()
        
        messages.success(request, 'Transferencia enviada correctamente')
        return redirect('transfer_detailGPT4', payment_id=payment_id)
        
    except Exception as e:
        LogTransferencia.objects.create(
            registro=transfer.payment_id,
            tipo_log='ERROR',
            contenido=f'Error al enviar transferencia: {str(e)}'
        )
        messages.error(request, f'Error al enviar transferencia: {str(e)}')
        return redirect('transfer_detailGPT4', payment_id=payment_id)

@login_required
def send_transfer_simulator_view_gpt4(request, payment_id):
    """Vista para enviar una transferencia al simulador."""
    transfer = get_object_or_404(Transfer, payment_id=payment_id)
    
    try:
        # Registrar el intento de envío
        LogTransferencia.objects.create(
            registro=transfer.payment_id,
            tipo_log='TRANSFER',
            contenido=f'Iniciando envío de transferencia {transfer.payment_id} al simulador'
        )
        
        # Actualizar estado
        transfer.status = 'ACSP'  # En proceso
        transfer.save()
        
        messages.success(request, 'Transferencia enviada al simulador correctamente')
        return redirect('transfer_detailGPT4', payment_id=payment_id)
        
    except Exception as e:
        LogTransferencia.objects.create(
            registro=transfer.payment_id,
            tipo_log='ERROR',
            contenido=f'Error al enviar transferencia al simulador: {str(e)}'
        )
        messages.error(request, f'Error al enviar transferencia al simulador: {str(e)}')
        return redirect('transfer_detailGPT4', payment_id=payment_id)

@login_required
def send_transfer_conexion_view_gpt4(request, payment_id):
    """Vista para enviar una transferencia al banco."""
    transfer = get_object_or_404(Transfer, payment_id=payment_id)
    
    try:
        # Registrar el intento de envío
        LogTransferencia.objects.create(
            registro=transfer.payment_id,
            tipo_log='TRANSFER',
            contenido=f'Iniciando envío de transferencia {transfer.payment_id} al banco'
        )
        
        # Actualizar estado
        transfer.status = 'ACSP'  # En proceso
        transfer.save()
        
        messages.success(request, 'Transferencia enviada al banco correctamente')
        return redirect('transfer_detailGPT4', payment_id=payment_id)
        
    except Exception as e:
        LogTransferencia.objects.create(
            registro=transfer.payment_id,
            tipo_log='ERROR',
            contenido=f'Error al enviar transferencia al banco: {str(e)}'
        )
        messages.error(request, f'Error al enviar transferencia al banco: {str(e)}')
        return redirect('transfer_detailGPT4', payment_id=payment_id)