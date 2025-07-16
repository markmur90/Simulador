from datetime import datetime, timedelta, timezone
import json
from django.utils import timezone
import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from .forms import (
    AccountMovementForm, UserCreateForm, UserUpdateForm
)
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import (
    Creditor,
    CreditorAccount,
    CreditorAgent,
    Debtor,
    DebtorAccount,
    AccountMovement,
    OficialBancario,
    OTPChallenge,
    PaymentIdentification,
    Transfer,
)
from .forms import UserCreateWithRoleForm
from django.utils.crypto import get_random_string
from services.transfer_services import TransferService
from django.core.exceptions import ValidationError
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from decimal import Decimal
import uuid
from django.contrib import messages
from django.core.exceptions import PermissionDenied

# Registros simples en memoria para OAuth y transferencias pendientes
OAUTH_APPROVED = {}
PENDING_TRANSFERS = {}

# @csrf_exempt
# def recibir_transferencia(request):
#     return JsonResponse({"error": "Funcionalidad deshabilitada"}, status=501)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        return render(request, "banco/login.html", {"error": "Credenciales inválidas"})
    return render(request, "banco/login.html")


@login_required
def dashboard_view(request):
    """Vista del dashboard con transferencias y cuentas"""
    
    # Obtener cuentas según el rol del usuario
    if request.user.groups.filter(name='Oficial Bancario').exists():
        debtor_accounts = DebtorAccount.objects.all()
        transfers = Transfer.objects.all()
    else:
        debtor_accounts = DebtorAccount.objects.filter(debtor__user=request.user)
        transfers = Transfer.objects.filter(
            Q(debtor_account__in=debtor_accounts) |
            Q(creditor_account__in=debtor_accounts)
        )

    # Ordenar transferencias por fecha
    transfers = transfers.order_by('-created_at')

    context = {
        'debtor_accounts': debtor_accounts,
        'transfers': transfers,
        'total_balance': sum(account.balance for account in debtor_accounts),
    }

    # Renderizar plantilla según el rol
    if request.user.is_superuser:
        template = 'banco/dashboard_superuser.html'
    elif request.user.groups.filter(name='Oficial Bancario').exists():
        template = 'banco/dashboard_oficial_bancario.html'
    elif request.user.groups.filter(name='Gerente').exists():
        template = 'banco/dashboard_gerente.html'
    elif request.user.groups.filter(name='Supervisor').exists():
        template = 'banco/dashboard_supervisor.html'
    elif request.user.groups.filter(name='Administrador').exists():
        template = 'banco/dashboard_administrador.html'
    else:
        template = 'banco/dashboard.html'

    return render(request, template, context)


@login_required
def transferencia_view(request):
    if request.method == "POST":
        destinatario = request.POST["destinatario"]
        monto = float(request.POST["monto"])
        # Aquí guardaríamos la transferencia
        return redirect("dashboard")
    return render(request, "banco/transferencia.html")


def registro_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "banco/registro.html", {"form": form})


@login_required
def logout_view(request):
    """End the current user session and redirect to login."""
    logout(request)
    return redirect("login")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_user_active(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        user.is_active = not user.is_active
        user.save()
    return redirect("user_management")


# banco/views.py
import jwt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import datetime, timedelta
from .models import OficialBancario

# Clave usada para firmar JWT desde vistas o comandos
JWT_SECRET = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
ALGORITHM = 'HS256'

@csrf_exempt
def generar_token(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    data = json.loads(request.body.decode())
    username = data.get('username')
    password = data.get('password')

    try:
        oficial = OficialBancario.objects.get(username=username)
        if not oficial.check_password(password):
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
    except OficialBancario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    payload = {
        'usuario': username,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return JsonResponse({'token': token})




def oauth2_authorize(request):
    """Endpoint de autorización simulado.

    Marca un ``payment_id`` como autorizado para posteriores
    operaciones protegidas por OAuth.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    payment_id = request.GET.get('payment_id')
    if not payment_id:
        return JsonResponse({'error': 'payment_id requerido'}, status=400)

    OAUTH_APPROVED[payment_id] = True
    return JsonResponse({'result': 'authorized', 'payment_id': payment_id})




# banco/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import OficialBancario  # o el modelo que uses
import json

@csrf_exempt
def crear_transferencia(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    if not hasattr(request, 'user_jwt'):
        return JsonResponse({'error': 'Autenticación requerida'}, status=401)

    data = json.loads(request.body.decode())
    monto = data.get('monto')
    destino = data.get('destino')

    usuario = request.user_jwt['usuario']
    oficial = OficialBancario.objects.get(username=usuario)

    # Validaciones básicas
    if not monto or not destino:
        return JsonResponse({'error': 'Faltan datos'}, status=400)

    # Lógica simulada eliminada
    return JsonResponse({'estado': 'ok', 'payment_id': 'SIMULATED'})

@csrf_exempt
def api_challenge(request):
    """
    POST /api/challenge
    Genera un nuevo desafío OTP para una transferencia.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        payment_id = data.get('payment_id')

        if not payment_id:
            return JsonResponse({'error': 'payment_id requerido'}, status=400)

        # Generar OTP
        challenge, otp = SecurityService.generate_otp_challenge(
            payment_id,
            request.user_jwt.get('usuario')
        )

        return JsonResponse({
            'challenge_id': str(challenge.challenge_id),
            'otp': otp
        })

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error interno'}, status=500)



import json
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

from .models import OficialBancario, OTPChallenge, Transfer
from .totp_utils import verify_totp
from services.transfer_services import TransferService
from services.security_services import SecurityService

# Clave y algoritmo para JWT
import jwt
JWT_SECRET = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
ALGORITHM = 'HS256'


@csrf_exempt
def login_api_simulador(request):
    """
    POST /api/login/
    --- Login de OficialBancario y creación de JWT válido
    Body: { "username": "...", "password": "..." }
    Response: { "token": "..." }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    try:
        oficial = OficialBancario.objects.get(username=username)
        if not oficial.check_password(password):
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
    except OficialBancario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    payload = {
        'usuario': username,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return JsonResponse({'token': token})


def _authenticate_jwt(request):
    """
    Lee el header Authorization, decodifica el JWT y devuelve payload o None.
    """
    auth = request.headers.get('Authorization', '').split()
    if len(auth) != 2 or auth[0].lower() != 'bearer':
        return None
    try:
        payload = jwt.decode(auth[1], JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


@csrf_exempt
def api_send_transfer(request):
    """
    POST /api/send-transfer
    Procesa una nueva transferencia con validación OTP.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        payment_id = data.get('payment_id')
        otp = data.get('otp')

        if not payment_id or not otp:
            return JsonResponse({'error': 'Faltan datos requeridos'}, status=400)

        # Verificar OTP
        try:
            SecurityService.verify_otp_challenge(payment_id, otp)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Obtener transferencia
        transfer = get_object_or_404(Transfer, payment_id=payment_id)
        
        # Actualizar estado
        transfer = TransferService.update_transfer_status(
            transfer,
            'ACCP',
            request.user_jwt.get('usuario')
        )

        return JsonResponse({
            'payment_id': transfer.payment_id,
            'status': transfer.status
        })

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error interno'}, status=500)

@csrf_exempt
def api_challenge(request):
    """
    POST /api/challenge
    Genera un nuevo desafío OTP para una transferencia.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        payment_id = data.get('payment_id')

        if not payment_id:
            return JsonResponse({'error': 'payment_id requerido'}, status=400)

        # Generar OTP
        challenge, otp = SecurityService.generate_otp_challenge(
            payment_id,
            request.user_jwt.get('usuario')
        )

        return JsonResponse({
            'challenge_id': str(challenge.challenge_id),
            'otp': otp
        })

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error interno'}, status=500)

@csrf_exempt
def api_transfer_incoming(request):
    """
    POST /api/transferencias/entrantes
    Procesa transferencias entrantes.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        
        # Crear transferencia
        transfer = TransferService.ingest_transfer(data)

        # Si requiere OTP, generar challenge
        if transfer.status == 'PDNG':
            challenge, otp = SecurityService.generate_otp_challenge(
                transfer.payment_id,
                request.user_jwt.get('usuario')
            )
            return JsonResponse({
                'payment_id': transfer.payment_id,
                'status': transfer.status,
                'challenge_id': str(challenge.challenge_id),
                'otp': otp,
                'otp_required': True
            })

        return JsonResponse({
            'payment_id': transfer.payment_id,
            'status': transfer.status,
            'otp_required': False
        })

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error interno'}, status=500)

@csrf_exempt
def api_status_transfer(request):
    """
    GET /api/status-transfer
    Consulta el estado de una transferencia.
    """
    payment_id = request.GET.get('payment_id')
    if not payment_id:
        return JsonResponse({'error': 'payment_id requerido'}, status=400)

    try:
        transfer = get_object_or_404(Transfer, payment_id=payment_id)
        return JsonResponse({
            'payment_id': transfer.payment_id,
            'status': transfer.status,
            'created_at': transfer.created_at.isoformat(),
            'updated_at': transfer.updated_at.isoformat()
        })
    except Exception as e:
        return JsonResponse({'error': 'Error interno'}, status=500)


def transfer_simulator_frontend(request):
    return render(request, 'banco/transfer_simulator_frontend.html')


# ---------------------------------------------------------------------------
# Gestión de usuarios (solo para superusuario)
# ---------------------------------------------------------------------------
@login_required
def user_list(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    users = User.objects.all()
    return render(request, 'banco/user_list.html', {'users': users})


@login_required
def user_create(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render(request, 'banco/user_form.html', {'form': form, 'create': True})


@login_required
def user_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboard')
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        initial = {'role': user.groups.first()}
        form = UserUpdateForm(instance=user, initial=initial)
    return render(request, 'banco/user_form.html', {'form': form, 'edit': True})


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserCreateWithRoleForm

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_management(request):
    users = User.objects.all()
    all_groups = Group.objects.all().order_by('name')
    if request.method == "POST":
        form = UserCreateWithRoleForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data["role"]
            user.groups.add(group)
            return redirect("user_management")
    else:
        form = UserCreateWithRoleForm()
    return render(request, "banco/user_management.html", {
        "form": form,
        "users": users,
        "all_groups": all_groups,
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_user_role(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        group_id = request.POST.get("group")
        user.groups.clear()
        if group_id:
            group = get_object_or_404(Group, pk=group_id)
            user.groups.add(group)
        messages.success(request, f"El rol de «{user.username}» se actualizó correctamente.")
    return redirect("user_management")


@login_required
def account_movement_create(request, account_id, tipo):
    """Registra un depósito o pago en una cuenta de deudor."""
    account = get_object_or_404(DebtorAccount, pk=account_id)
    if request.method == "POST":
        form = AccountMovementForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.account = account
            movimiento.tipo = tipo
            movimiento.save()
            return redirect('estado_cuenta', account_id=account.id)
    else:
        form = AccountMovementForm(initial={'tipo': tipo})
    return render(request, 'banco/movimiento_form.html', {
        'form': form,
        'account': account,
        'tipo': tipo,
    })


@login_required
def estado_cuenta(request, account_id):
    """Muestra el estado de cuenta de una cuenta de deudor."""
    account = get_object_or_404(DebtorAccount, pk=account_id)
    movimientos = account.movimientos.order_by('-fecha')
    start = request.GET.get('inicio')
    end = request.GET.get('fin')
    if start:
        movimientos = movimientos.filter(fecha__date__gte=start)
    if end:
        movimientos = movimientos.filter(fecha__date__lte=end)
    return render(request, 'banco/estado_deudor.html', {
        'account': account,
        'movimientos': movimientos,
    })


@login_required
def estado_cuenta_pdf(request, account_id):
    """Exporta el estado de cuenta en PDF."""
    account = get_object_or_404(DebtorAccount, pk=account_id)
    movimientos = account.movimientos.order_by('fecha')
    start = request.GET.get('inicio')
    end = request.GET.get('fin')
    if start:
        movimientos = movimientos.filter(fecha__date__gte=start)
    if end:
        movimientos = movimientos.filter(fecha__date__lte=end)

    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Estado de cuenta de {account.debtor.name}")
    y = 720
    for mov in movimientos:
        p.drawString(80, y, f"{mov.fecha.strftime('%Y-%m-%d %H:%M')} - {mov.tipo} - {mov.monto}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 750
    p.drawString(80, y-20, f"Saldo actual: {account.balance}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='estado.pdf')




from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Transfer
from services.transfer_services import TransferService
from .totp_utils import verify_totp

@csrf_exempt
def api_ingest_transfer(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    # 1) Validar JWT Simulador en Authorization: Bearer <token>
    auth = request.headers.get('Authorization','').split()
    if len(auth)!=2 or auth[0].lower()!='bearer':
        return JsonResponse({'error':'No autenticado'}, status=401)
    # Aquí decodificar jwt con JWT_SECRET, omitted

    data = json.loads(request.body)
    try:
        # Ingiere y crea la transferencia en PDNG o RJCT
        transfer = TransferService.ingest_transfer(data)
    except Exception as e:
        return JsonResponse({'status':'error','message':str(e)}, status=400)

    # 2) Respuesta inicial: pedimos OTP
    return JsonResponse({
        'transfer_id': transfer.id,
        'status': transfer.status,
        'otp_required': transfer.status=='PDNG',
    })

@csrf_exempt
def api_verify_otp(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Sólo POST'}, status=405)

    # El middleware JWTAuthenticationMiddleware habrá puesto el payload aquí
    payload = getattr(request, 'user_jwt', None)
    if not payload:
        return JsonResponse({'error': 'Autenticación requerida'}, status=401)

    data = json.loads(request.body)
    payment_id = data.get('payment_id')
    otp = data.get('otp')

    # Verificar desafío OTP
    try:
        challenge = OTPChallenge.objects.get(
            payment_id=payment_id, otp=otp, status='CREATED'
        )
    except OTPChallenge.DoesNotExist:
        return JsonResponse({'error': 'OTP inválido'}, status=400)

    challenge.status = 'USED'
    challenge.save()

    # Asegurar que exista la transferencia antes de completarla
    try:
        transfer = Transfer.objects.get(payment_id=payment_id)
    except Transfer.DoesNotExist:
        # Creación mínima de entidades para no violar FK
        debtor = Debtor.objects.first() or Debtor.objects.create(
            name="Dummy Debtor",
            customer_id="DUMMYCU001",
            address="Calle Falsa 123"
        )
        creditor = Creditor.objects.first() or Creditor.objects.create(
            name="Dummy Creditor",
            customer_id="CRDTCU001",
            address="Avenida Siempre Viva 742"
        )
        debtor_account = DebtorAccount.objects.filter(debtor=debtor).first() or DebtorAccount.objects.create(
            debtor=debtor,
            iban="XX001234560000000000",
            currency="EUR"
        )
        creditor_account = CreditorAccount.objects.filter(creditor=creditor).first() or CreditorAccount.objects.create(
            creditor=creditor,
            iban="XX009876540000000000",
            currency="EUR"
        )
        creditor_agent = CreditorAgent.objects.first() or CreditorAgent.objects.create(
            bic="DEUTDEFF",
            financial_institution_id="BANKDEFF"
        )
        payment_ident = PaymentIdentification.objects.create(
            end_to_end_id=str(payment_id)[:35],
            instruction_id=str(payment_id)[:35]
        )
        transfer = Transfer.objects.create(
            payment_id=payment_id,
            debtor=debtor,
            creditor=creditor,
            debtor_account=debtor_account,
            creditor_account=creditor_account,
            creditor_agent=creditor_agent,
            instructed_amount=1,
            currency=debtor_account.currency,
            purpose_code='GDSV',
            requested_execution_date=timezone.now().date(),
            payment_identification=payment_ident,
            status='PDNG'
        )

    # Finalizar la transferencia
    transfer.status = 'ACCP'
    transfer.auth_id = payload.get('usuario')
    transfer.save()

    return JsonResponse({
        'status': transfer.status,
        'transfer_id': transfer.payment_id
    })

@login_required
def transfer_view(request):
    """Vista para realizar transferencias internas y externas"""
    if request.method == "POST":
        try:
            # Obtener datos del formulario
            debtor_account_id = request.POST.get('debtor_account_id')
            creditor_account_id = request.POST.get('creditor_account_id')
            amount = Decimal(request.POST.get('amount', '0'))
            description = request.POST.get('description', '')
            transfer_type = request.POST.get('transfer_type')  # 'internal' o 'external'

            # Validar datos básicos
            if not all([debtor_account_id, creditor_account_id, amount]):
                raise ValidationError('Todos los campos son requeridos')

            if amount <= 0:
                raise ValidationError('El monto debe ser mayor a 0')

            # Obtener la cuenta deudora
            try:
                debtor_account = DebtorAccount.objects.get(id=debtor_account_id)
            except DebtorAccount.DoesNotExist:
                raise ValidationError('Cuenta deudora no encontrada')

            # Verificar que la cuenta pertenezca al usuario actual
            if not request.user.groups.filter(name='Oficial Bancario').exists():
                if debtor_account.debtor.user != request.user:
                    raise ValidationError('No tienes permiso para usar esta cuenta')

            # Validar saldo suficiente
            if debtor_account.balance < amount:
                raise ValidationError('Saldo insuficiente')

            # Generar payment_id único
            payment_id = str(uuid.uuid4())

            # Preparar datos para la transferencia
            transfer_data = {
                'payment_id': payment_id,
                'debtor_account': debtor_account.iban,
                'instructed_amount': amount,
                'currency': debtor_account.currency,
                'description': description
            }

            if transfer_type == 'internal':
                # Transferencia entre cuentas propias
                try:
                    creditor_account = DebtorAccount.objects.get(id=creditor_account_id)
                    if creditor_account.debtor != debtor_account.debtor:
                        raise ValidationError('La cuenta destino no pertenece al mismo titular')
                    
                    transfer_data['creditor_account'] = creditor_account.iban
                except DebtorAccount.DoesNotExist:
                    raise ValidationError('Cuenta destino no encontrada')

            else:
                # Transferencia externa
                try:
                    creditor_account = CreditorAccount.objects.get(id=creditor_account_id)
                    transfer_data['creditor_account'] = creditor_account.iban
                except CreditorAccount.DoesNotExist:
                    raise ValidationError('Cuenta destino no encontrada')

            # Crear la transferencia
            transfer = TransferService.create_transfer(transfer_data)

            # Procesar inmediatamente si es interna
            if transfer_type == 'internal':
                TransferService.process_transfer(transfer)
                messages.success(request, 'Transferencia interna realizada con éxito')
            else:
                # Para transferencias externas, iniciar el proceso de autorización
                messages.info(request, 'Transferencia externa creada. Pendiente de autorización')

            return redirect('dashboard')

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'Error al procesar la transferencia')
            
    # GET: Mostrar formulario
    context = {
        'debtor_accounts': DebtorAccount.objects.filter(
            debtor__user=request.user
        ) if not request.user.groups.filter(name='Oficial Bancario').exists() else DebtorAccount.objects.all(),
        'creditor_accounts': CreditorAccount.objects.all()
    }
    return render(request, 'banco/transfer_form.html', context)

@login_required
def transfer_status_view(request, payment_id):
    """Vista para mostrar el estado de una transferencia"""
    try:
        transfer = get_object_or_404(Transfer, payment_id=payment_id)
        
        # Verificar permisos
        if not request.user.groups.filter(name='Oficial Bancario').exists():
            if transfer.debtor_account.debtor.user != request.user:
                raise PermissionDenied
        
        return render(request, 'banco/transfer_status.html', {
            'transfer': transfer
        })
    except Transfer.DoesNotExist:
        messages.error(request, 'Transferencia no encontrada')
        return redirect('dashboard')

@login_required
def api_transfer_status(request, payment_id):
    """API para consultar el estado de una transferencia"""
    try:
        transfer = get_object_or_404(Transfer, payment_id=payment_id)
        
        # Verificar permisos
        if not request.user.groups.filter(name='Oficial Bancario').exists():
            if transfer.debtor_account.debtor.user != request.user:
                return JsonResponse({'error': 'No autorizado'}, status=403)
        
        return JsonResponse(TransferService.get_transfer_status(payment_id))
    except Transfer.DoesNotExist:
        return JsonResponse({'error': 'Transferencia no encontrada'}, status=404)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error interno'}, status=500)
