from datetime import datetime, timedelta
import json

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import (
    DebtorSimulado,
    CreditorSimulado,
    TransferenciaSimulada,
    OficialBancario,
    OTPChallenge,
)
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
    return render(request, "banco/dashboard.html", {"saldo": saldo})


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

    return JsonResponse({'estado': 'ok', 'id': t.id})

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