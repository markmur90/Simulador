import json
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

from .models import OficialBancario, OTPChallenge, Transfer
from .totp_utils import verify_totp
from services.transfer_services import TransferService

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
    POST /api/transferencia/
    --- Recibe datos SEPA, crea la transferencia en PDNG y devuelve challenge OTP.
    Body JSON: según esquema SEPA.
    Response:
      {
        "payment_id": "...",
        "status": "PDNG",
        "challenge_id": "...",
        "otp_required": true
      }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    # Autenticación JWT
    payload = _authenticate_jwt(request)
    if not payload:
        return JsonResponse({'error': 'Autenticación requerida'}, status=401)

    data = json.loads(request.body)
    try:
        transfer = TransferService.ingest_transfer(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    # Generar OTP y registrar challenge
    otp_code = get_random_string(6, allowed_chars='0123456789')
    challenge = OTPChallenge.objects.create(
        transfer=transfer,
        payment_id=transfer.payment_id,
        otp=otp_code,
        status='CREATED'
    )

    return JsonResponse({
        'payment_id': transfer.payment_id,
        'status': transfer.status,
        'challenge_id': str(challenge.challenge_id),
        'otp_required': True
    }, status=202)


@csrf_exempt
def api_verify_otp(request):
    """
    POST /api/transferencia/verify/
    --- Recibe payment_id y otp, valida y finaliza la transferencia.
    Body: { "payment_id": "...", "otp": "123456" }
    Response: { "status": "ACSC", "transfer_id": "..." }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Sólo POST'}, status=405)

    payload = _authenticate_jwt(request)
    if not payload:
        return JsonResponse({'error': 'Autenticación requerida'}, status=401)

    data = json.loads(request.body)
    payment_id = data.get('payment_id')
    otp = data.get('otp')

    # Verificar challenge existente
    try:
        challenge = OTPChallenge.objects.get(
            payment_id=payment_id,
            otp=otp,
            status='CREATED'
        )
    except OTPChallenge.DoesNotExist:
        return JsonResponse({'error': 'OTP inválido'}, status=400)

    # Marcar challenge como usado
    challenge.status = 'USED'
    challenge.save()

    # Actualizar estado de la transferencia
    try:
        transfer = Transfer.objects.get(payment_id=payment_id)
    except Transfer.DoesNotExist:
        return JsonResponse({'error': 'payment_id no válido'}, status=404)

    transfer.status = 'ACSC'
    transfer.save()

    return JsonResponse({
        'status': transfer.status,
        'transfer_id': transfer.payment_id
    })
