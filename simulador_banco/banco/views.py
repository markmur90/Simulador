from datetime import datetime, timedelta
import json

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from .forms import (
    UserCreateForm, UserUpdateForm,
    DebtorSimuladoForm, CreditorSimuladoForm, TransferenciaSimuladaForm
)
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import (
    DebtorSimulado,
    CreditorSimulado,
    TransferenciaSimulada,
    OficialBancario,
    OTPChallenge,
)
from .forms import UserCreateWithRoleForm
from django.utils.crypto import get_random_string
from services.transfer_services import TransferService
from django.core.exceptions import ValidationError

@csrf_exempt
def recibir_transferencia(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            campos = ["paymentIdentification", "debtor", "creditor", "instructedAmount"]
            if not all(field in data for field in campos):
                return JsonResponse({"estado": "RJCT", "mensaje": "Campos faltantes"}, status=400)

            debtor_name = data["debtor"].get("name")
            creditor_name = data["creditor"].get("name")
            monto = float(data["instructedAmount"].get("amount"))

            debtor, _ = DebtorSimulado.objects.get_or_create(nombre=debtor_name)
            creditor, _ = CreditorSimulado.objects.get_or_create(nombre=creditor_name)

            TransferenciaSimulada.objects.create(
                payment_id=data["paymentIdentification"],
                debtor=debtor,
                creditor=creditor,
                monto=monto
            )

            return JsonResponse({"estado": "ACSC", "mensaje": "Transferencia aceptada"}, status=200)

        except Exception as e:
            return JsonResponse({"estado": "ERRO", "mensaje": str(e)}, status=500)

    return JsonResponse({"mensaje": "Solo POST permitido"}, status=405)


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
    saldo = 10000  # Simulado por ahora
    user = request.user
    template = "banco/dashboard_oficial.html"
    if user.is_superuser:
        template = "banco/dashboard_superuser.html"
    elif user.groups.filter(name="Supervisor").exists():
        template = "banco/dashboard_supervisor.html"
    elif user.groups.filter(name="Gerente").exists():
        template = "banco/dashboard_gerente.html"
    elif user.groups.filter(name="Administrador").exists():
        template = "banco/dashboard_administrador.html"
    return render(request, template, {"saldo": saldo})


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
    username = data.get('usuario')
    password = data.get('clave')

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




# banco/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import TransferenciaSimulada, OficialBancario  # o el modelo que uses
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

    # Crear y guardar transferencia
    t = TransferenciaSimulada(oficial=oficial, monto=monto, destino=destino)
    t.save()

    return JsonResponse({'estado': 'ok', 'payment_id': t.payment_id})

@csrf_exempt
def api_challenge(request):
    """Genera un OTP para una transferencia simulada."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    if not hasattr(request, 'user_jwt'):
        return JsonResponse({'error': 'Autenticación requerida'}, status=401)

    data = json.loads(request.body.decode())
    payment_id = data.get('payment_id')
    if not payment_id:
        return JsonResponse({'error': 'payment_id requerido'}, status=400)

    otp = get_random_string(6, allowed_chars='0123456789')
    challenge = OTPChallenge.objects.create(payment_id=payment_id, otp=otp)
    return JsonResponse({'challenge_id': str(challenge.challenge_id), 'otp': otp})


@csrf_exempt
def api_send_transfer(request):
    """Procesa la transferencia validando el OTP."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    if not hasattr(request, 'user_jwt'):
        return JsonResponse({'error': 'Autenticación requerida'}, status=401)

    data = json.loads(request.body.decode())
    payment_id = data.get('payment_id')
    otp = data.get('otp')
    totp_code = data.get('totp')

    from .totp_utils import verify_totp
    if not verify_totp(str(totp_code)):
        return JsonResponse({'error': 'TOTP inválido'}, status=400)
    
    try:
        challenge = OTPChallenge.objects.get(payment_id=payment_id, otp=otp, status='CREATED')
    except OTPChallenge.DoesNotExist:
        return JsonResponse({'error': 'OTP inválido'}, status=400)

    challenge.status = 'USED'
    challenge.save()

    TransferenciaSimulada.objects.get_or_create(
        payment_id=payment_id,
        defaults={'debtor': DebtorSimulado.objects.first(),
                 'creditor': CreditorSimulado.objects.first(),
                 'monto': 0}
    )

    return JsonResponse({'transactionStatus': 'ACSC', 'authId': str(challenge.challenge_id)})


def api_status_transfer(request):
    payment_id = request.GET.get('payment_id')
    if not payment_id:
        return JsonResponse({'error': 'payment_id requerido'}, status=400)
    exists = TransferenciaSimulada.objects.filter(payment_id=payment_id).exists()
    status = 'ACSC' if exists else 'RJCT'
    return JsonResponse({'payment_id': payment_id, 'status': status})


def transfer_simulator_frontend(request):
    return render(request, 'banco/transfer_simulator_frontend.html')

@csrf_exempt
def api_transfer_incoming(request):
    """Recibe transferencias de sistemas externos"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    # Autenticación mediante JWT o sesión activa
    if not hasattr(request, 'user_jwt') and not request.user.is_authenticated:
        return JsonResponse({'error': 'Autenticación requerida'}, status=401)

    try:
        data = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    try:
        transfer = TransferService.ingest_transfer(data)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'payment_id': transfer.payment_id, 'status': transfer.status})


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


# ---------------------------------------------------------------------------
# Vistas para modelos simulados (solo superusuario)
# ---------------------------------------------------------------------------
@login_required
def sim_debtor_list(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    objects = DebtorSimulado.objects.all()
    return render(request, 'banco/sim_debtor_list.html', {'objects': objects})


@login_required
def sim_debtor_create(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        form = DebtorSimuladoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sim_debtor_list')
    else:
        form = DebtorSimuladoForm()
    return render(request, 'banco/sim_debtor_form.html', {'form': form})


@login_required
def sim_creditor_list(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    objects = CreditorSimulado.objects.all()
    return render(request, 'banco/sim_creditor_list.html', {'objects': objects})


@login_required
def sim_creditor_create(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CreditorSimuladoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sim_creditor_list')
    else:
        form = CreditorSimuladoForm()
    return render(request, 'banco/sim_creditor_form.html', {'form': form})


@login_required
def sim_transfer_list(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    objects = TransferenciaSimulada.objects.all()
    return render(request, 'banco/sim_transfer_list.html', {'objects': objects})


@login_required
def sim_transfer_create(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        form = TransferenciaSimuladaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sim_transfer_list')
    else:
        form = TransferenciaSimuladaForm()
    return render(request, 'banco/sim_transfer_form.html', {'form': form})


from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
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

