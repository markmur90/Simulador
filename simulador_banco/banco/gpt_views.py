import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import uuid
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
import traceback

logger = logging.getLogger(__name__)

from .models import (
    ClientID, CreditorAgent, Debtor, DebtorAccount, Creditor, CreditorAccount, Kid,
    Transfer, AccountMovement, LogTransferencia, PaymentIdentification, PostalAddress,
    OTPChallenge
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
        logger.debug(f"Generando URL de éxito para payment_id: {self.object.payment_id}")
        return reverse_lazy('transfer_detailGPT4', kwargs={'payment_id': self.object.payment_id})

    def form_valid(self, form):
        logger.debug("Iniciando form_valid en TransferCreateView")
        logger.debug(f"Headers de la petición: {self.request.headers}")
        logger.debug(f"Método de la petición: {self.request.method}")
        logger.debug(f"Datos del formulario: {form.cleaned_data}")
        
        try:
            with transaction.atomic():
                logger.debug("Iniciando transacción atómica")
                # Validar saldo suficiente
                debtor_account = form.cleaned_data['debtor_account']
                amount = form.cleaned_data['instructed_amount']
                
                logger.debug(f"Validando saldo - Cuenta: {debtor_account.iban}, Saldo: {debtor_account.balance}, Monto solicitado: {amount}")
                
                if debtor_account.balance < amount:
                    logger.debug("Error: Saldo insuficiente")
                    if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        response_data = {
                            'error': 'Saldo insuficiente en la cuenta origen'
                        }
                        logger.debug(f"Enviando respuesta JSON: {response_data}")
                        return JsonResponse(response_data, status=400)
                    form.add_error(None, 'Saldo insuficiente en la cuenta origen')
                    return self.form_invalid(form)

                # Preparar datos para TransferService
                transfer_data = {
                    'debtor': form.cleaned_data['debtor'],
                    'debtor_account_id': debtor_account.id,
                    'creditor': form.cleaned_data['creditor'],
                    'creditor_account': form.cleaned_data['creditor_account'],
                    'creditor_agent': form.cleaned_data['creditor_agent'],
                    'instructed_amount': amount,
                    'currency': form.cleaned_data['currency'],
                    'purpose_code': form.cleaned_data['purpose_code'],
                    'requested_execution_date': form.cleaned_data['requested_execution_date'],
                    'remittance_information_unstructured': form.cleaned_data['remittance_information_unstructured'],
                }

                logger.debug(f"Datos preparados para TransferService: {transfer_data}")

                # Usar TransferService para procesar la transferencia
                from services.transfer_services import TransferService
                logger.debug("Llamando a TransferService.ingest_transfer")
                self.object = TransferService.ingest_transfer(transfer_data)
                logger.debug(f"Transferencia creada con payment_id: {self.object.payment_id}")

                if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    response_data = {
                        'status': 'success',
                        'payment_id': self.object.payment_id,
                    }
                    
                    # Si la transferencia requiere OTP, incluir la información necesaria
                    if self.object.status == 'PDNG':
                        logger.debug("Transferencia requiere OTP")
                        response_data.update({
                            'otp_required': True,
                            'redirect_url': reverse_lazy('transfer_sca', kwargs={'payment_id': self.object.payment_id})
                        })
                    else:
                        logger.debug("Transferencia no requiere OTP")
                        response_data.update({
                            'redirect_url': self.get_success_url()
                        })
                    
                    return JsonResponse(response_data)

                # Si la transferencia requiere OTP, redirigir a la página de verificación
                if self.object.status == 'PDNG':
                    logger.debug("Redirigiendo a verificación OTP")
                    messages.info(self.request, 'Se requiere verificación OTP para completar la transferencia')
                    return redirect('transfer_sca', payment_id=self.object.payment_id)
                
                logger.debug("Transferencia creada exitosamente")
                messages.success(self.request, 'Transferencia SEPA creada exitosamente')
                return super().form_valid(form)

        except Exception as e:
            import traceback
            logger.error("Error en TransferCreateView:")
            logger.error(f"Tipo de error: {type(e).__name__}")
            logger.error(f"Mensaje de error: {str(e)}")
            logger.error("Traceback completo:")
            logger.error(traceback.format_exc())
            
            # Registrar el error
            error_id = str(uuid.uuid4())
            LogTransferencia.objects.create(
                registro=error_id,
                tipo_log='ERROR',
                contenido=f'Error al crear transferencia SEPA: {str(e)}\n{traceback.format_exc()}'
            )
            
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                response_data = {
                    'error': f'Error al procesar la transferencia: {str(e)}'
                }
                logger.debug(f"Enviando respuesta de error JSON: {response_data}")
                return JsonResponse(response_data, status=500)
            messages.error(self.request, f'Error al procesar la transferencia: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.debug("Formulario inválido en TransferCreateView")
        logger.debug(f"Errores del formulario: {form.errors}")
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'Datos de formulario inválidos',
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        logger.debug("Obteniendo context data en TransferCreateView")
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Transferencia Interna'
        return context

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
    template_name = 'banco/gpt4/create_transfer_internal.html'
    form_class = TransferInternaForm
    
    def get_success_url(self):
        return reverse_lazy('transfer_detailGPT4', kwargs={'payment_id': self.object.payment_id})

    def get_debtor_accounts(self, debtor_id):
        """Obtener las cuentas de un deudor específico"""
        return DebtorAccount.objects.filter(debtor_id=debtor_id)

    def form_valid(self, form):
        logger.debug("Iniciando form_valid en TransferInternaCreateView")
        logger.debug(f"Datos del formulario: {form.cleaned_data}")
        
        try:
            with transaction.atomic():
                # Obtener los datos del formulario
                cuenta_origen = form.cleaned_data['cuenta_origen']
                cuenta_destino = form.cleaned_data['cuenta_destino']
                monto = form.cleaned_data['monto']
                concepto = form.cleaned_data['concepto']
                debtor_origen = form.cleaned_data['debtor_origen']
                debtor_destino = form.cleaned_data['debtor_destino']
                
                logger.debug(f"Cuenta origen: {cuenta_origen.iban}, Saldo: {cuenta_origen.balance}")
                logger.debug(f"Cuenta destino: {cuenta_destino.iban}")
                logger.debug(f"Monto: {monto}")
                
                # Validar saldo suficiente
                if cuenta_origen.balance < monto:
                    logger.warning(f"Saldo insuficiente. Saldo: {cuenta_origen.balance}, Monto: {monto}")
                    form.add_error(None, 'Saldo insuficiente en la cuenta origen')
                    return self.form_invalid(form)

                # Generar payment_id único
                payment_id = str(uuid.uuid4())

                # Crear PaymentIdentification
                payment_identification = PaymentIdentification.objects.create(
                    end_to_end_id=str(uuid.uuid4()),
                    instruction_id=str(uuid.uuid4())
                )
                logger.debug(f"PaymentIdentification creado: {payment_identification.id}")

                # Crear o obtener un Creditor basado en el Debtor destino
                creditor, created = Creditor.objects.get_or_create(
                    name=debtor_destino.name,
                    defaults={
                        'address': PostalAddress.objects.create(
                            country='ES',
                            street=debtor_destino.address.street if hasattr(debtor_destino, 'address') else '',
                            city=debtor_destino.address.city if hasattr(debtor_destino, 'address') else ''
                        )
                    }
                )

                # Crear o obtener CreditorAccount basada en la cuenta destino
                creditor_account, created = CreditorAccount.objects.get_or_create(
                    creditor=creditor,
                    iban=cuenta_destino.iban,
                    defaults={
                        'currency': cuenta_destino.currency
                    }
                )

                # Obtener o crear CreditorAgent
                creditor_agent, created = CreditorAgent.objects.get_or_create(
                    bic='INTERNALBIC',
                    defaults={
                        'financial_institution_id': 'INTERNAL_BANK',
                        'other_information': 'Banco Interno para Transferencias Internas'
                    }
                )

                # Crear la transferencia
                self.object = Transfer.objects.create(
                    debtor=debtor_origen,
                    creditor=creditor,
                    debtor_account=cuenta_origen,
                    creditor_account=creditor_account,
                    creditor_agent=creditor_agent,
                    instructed_amount=monto,
                    currency=cuenta_origen.currency,
                    purpose_code='GDSV',
                    requested_execution_date=timezone.now().date(),
                    remittance_information_unstructured=concepto,
                    status='PDNG',
                    payment_identification=payment_identification
                )
                logger.debug(f"Transferencia creada con payment_id: {self.object.payment_id}")

                # Usar TransferService para procesar la transferencia
                from services.transfer_services import TransferService
                self.object = TransferService.process_transfer(self.object)
                logger.debug(f"Transferencia procesada. Estado final: {self.object.status}")

                # Si es una petición AJAX, devolver JSON
                if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'payment_id': self.object.payment_id,
                        'redirect_url': self.get_success_url()
                    })
                
                # Si no es AJAX, redirigir normalmente
                return HttpResponseRedirect(self.get_success_url())

        except Exception as e:
            logger.error(f"Error en form_valid: {str(e)}")
            form.add_error(None, f'Error al procesar la transferencia: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.warning("Formulario inválido")
        logger.warning(f"Errores del formulario: {form.errors}")
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
        
        return super().form_invalid(form)

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

class TransferSCAView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'api/GPT4/transfer_sca.html'

    def get_context_data(self, **kwargs):
        logger.debug("Obteniendo context data en TransferSCAView")
        context = super().get_context_data(**kwargs)
        payment_id = self.kwargs.get('payment_id')
        transfer = get_object_or_404(Transfer, payment_id=payment_id)
        context['transfer'] = transfer
        
        # Buscar el challenge OTP activo
        otp_challenge = OTPChallenge.objects.filter(
            payment_id=payment_id,
            status='CREATED'
        ).first()
        
        if otp_challenge:
            logger.debug(f"OTP Challenge encontrado para payment_id: {payment_id}")
        else:
            logger.debug(f"No se encontró OTP Challenge para payment_id: {payment_id}")
            
        context['otp_challenge'] = otp_challenge
        return context

    def post(self, request, *args, **kwargs):
        logger.debug("Procesando POST en TransferSCAView")
        payment_id = self.kwargs.get('payment_id')
        otp_code = request.POST.get('otp')
        
        try:
            challenge = OTPChallenge.objects.get(
                payment_id=payment_id,
                status='CREATED'
            )
            
            if challenge.otp != otp_code:
                logger.debug(f"Código OTP inválido para payment_id: {payment_id}")
                messages.error(request, 'Código OTP inválido')
                return self.render_to_response(self.get_context_data())
            
            # Marcar el challenge como usado
            challenge.status = 'USED'
            challenge.save()
            
            # Actualizar el estado de la transferencia
            transfer = Transfer.objects.get(payment_id=payment_id)
            transfer.status = 'ACCP'
            transfer.save()
            
            logger.debug(f"Transferencia {payment_id} verificada exitosamente")
            messages.success(request, 'Transferencia verificada exitosamente')
            return redirect('transfer_detailGPT4', payment_id=payment_id)
            
        except OTPChallenge.DoesNotExist:
            logger.error(f"Desafío OTP no encontrado para payment_id: {payment_id}")
            messages.error(request, 'Desafío OTP no encontrado o ya utilizado')
            return self.render_to_response(self.get_context_data())
        except Exception as e:
            logger.error(f"Error al verificar la transferencia: {str(e)}")
            messages.error(request, f'Error al verificar la transferencia: {str(e)}')
            return self.render_to_response(self.get_context_data())