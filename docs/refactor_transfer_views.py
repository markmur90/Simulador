# refactored_views.py
import json
import uuid
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from utils.jwt_utils import decode_jwt
from services.transfer_service import TransferService
from models import OTPChallenge, Transfer
from .forms import TransferenciaForm, OTPConfirmForm


def validate_transfer_payload(data):
    required_fields = ["debtor_account_id", "creditor_account_id", "amount", "iban"]
    for field in required_fields:
        if field not in data:
            return False, f"Campo obligatorio ausente: {field}"
    try:
        float(data["amount"])
    except ValueError:
        return False, "Monto inválido"
    return True, ""


def log_event(event_type, reference, message):
    # Aquí iría la lógica para registrar logs estructurados
    print(f"[{event_type}] {reference}: {message}")


@login_required
def enviar_transferencia_form(request):
    if request.method == "POST":
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            transfer, otp = TransferService.ingest_transfer(data, user=request.user)
            log_event("TRANSFER_INITIATED", transfer.payment_id, f"OTP generado: {otp}")
            return render(request, "otp_confirm.html", {"payment_id": transfer.payment_id, "otp": otp})
    else:
        form = TransferenciaForm()
    return render(request, "transfer_form.html", {"form": form})


@login_required
def confirmar_transferencia_form(request):
    if request.method == "POST":
        form = OTPConfirmForm(request.POST)
        if form.is_valid():
            payment_id = form.cleaned_data["payment_id"]
            otp = form.cleaned_data["otp"]
            challenge = OTPChallenge.objects.filter(payment_id=payment_id, otp=otp, estado="CREATED").first()
            if not challenge:
                return render(request, "otp_confirm.html", {"error": "OTP inválido", "payment_id": payment_id})

            challenge.estado = "USED"
            challenge.used_at = timezone.now()
            challenge.save()

            transfer = Transfer.objects.filter(payment_id=payment_id).first()
            if not transfer:
                return render(request, "otp_confirm.html", {"error": "Transferencia no encontrada", "payment_id": payment_id})

            result = TransferService.complete_transfer(transfer, user=request.user)
            log_event("TRANSFER_COMPLETED", payment_id, f"Estado: {result['status']}")
            return render(request, "transfer_result.html", result)
    return HttpResponseRedirect("/")


@csrf_exempt
@require_POST
def api_send_transfer(request):
    try:
        token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        user = decode_jwt(token)
        if not user:
            return JsonResponse({"error": "Token inválido"}, status=401)

        data = json.loads(request.body)
        valid, msg = validate_transfer_payload(data)
        if not valid:
            return JsonResponse({"error": msg}, status=400)

        transfer, otp = TransferService.ingest_transfer(data, user=user)
        log_event("TRANSFER_INITIATED", transfer.payment_id, f"OTP generado: {otp}")

        return JsonResponse({
            "payment_id": transfer.payment_id,
            "status": transfer.status,
            "otp_required": True,
            "challenge_id": transfer.payment_id
        }, status=202)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_POST
def api_verify_otp(request):
    try:
        token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        user = decode_jwt(token)
        if not user:
            return JsonResponse({"error": "Token inválido"}, status=401)

        data = json.loads(request.body)
        payment_id = data.get("payment_id")
        otp = data.get("otp")
        if not payment_id or not otp:
            return JsonResponse({"error": "Faltan datos"}, status=400)

        challenge = OTPChallenge.objects.filter(payment_id=payment_id, otp=otp, estado="CREATED").first()
        if not challenge:
            return JsonResponse({"error": "OTP inválido"}, status=403)

        challenge.estado = "USED"
        challenge.used_at = timezone.now()
        challenge.save()

        transfer = Transfer.objects.filter(payment_id=payment_id).first()
        if not transfer:
            return JsonResponse({"error": "Transferencia no encontrada"}, status=404)

        result = TransferService.complete_transfer(transfer, user=user)
        log_event("TRANSFER_COMPLETED", payment_id, f"Estado: {result['status']}")

        return JsonResponse(result, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def api_transfer_status(request, payment_id):
    transfer = Transfer.objects.filter(payment_id=payment_id).first()
    if not transfer:
        return JsonResponse({"error": "Transferencia no encontrada"}, status=404)

    return JsonResponse({
        "payment_id": transfer.payment_id,
        "status": transfer.status,
        "monto": str(transfer.amount),
        "deudor": transfer.debtor_account_id,
        "acreedor": transfer.creditor_account_id
    })


# forms.py
from django import forms

class TransferenciaForm(forms.Form):
    debtor_account_id = forms.CharField(label="ID Cuenta Deudora", max_length=100)
    creditor_account_id = forms.CharField(label="ID Cuenta Acreedora", max_length=100)
    amount = forms.DecimalField(label="Monto", min_value=0.01, max_digits=10, decimal_places=2)
    iban = forms.CharField(label="IBAN", max_length=34)

class OTPConfirmForm(forms.Form):
    payment_id = forms.CharField(widget=forms.HiddenInput())
    otp = forms.CharField(label="Código OTP", max_length=6)
