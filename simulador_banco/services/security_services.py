from django.core.exceptions import ValidationError
from django.utils import timezone
from banco.models import OTPChallenge, LogTransferencia
import pyotp
from typing import Optional

class SecurityService:
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 5
    MAX_OTP_ATTEMPTS = 3

    @classmethod
    def generate_otp_challenge(cls, payment_id: str, auth_id: Optional[str] = None) -> OTPChallenge:
        """Genera un nuevo desafío OTP."""
        # Generar OTP
        totp = pyotp.TOTP(pyotp.random_base32())
        otp = totp.now()

        # Crear challenge
        challenge = OTPChallenge.objects.create(
            payment_id=payment_id,
            otp=otp,
            auth_id=auth_id,
            expires_at=timezone.now() + timezone.timedelta(minutes=cls.OTP_EXPIRY_MINUTES),
            attempts=0
        )

        LogTransferencia.objects.create(
            registro=payment_id,
            tipo_log='OTP',
            contenido=f'Challenge generado: {challenge.challenge_id}'
        )

        return challenge

    @classmethod
    def verify_otp_challenge(
        cls,
        payment_id: str,
        otp: str,
        auth_id: Optional[str] = None
    ) -> OTPChallenge:
        """Verifica un desafío OTP."""
        try:
            challenge = OTPChallenge.objects.get(
                payment_id=payment_id,
                status__in=['CREATED', 'ATTEMPTED']
            )
        except OTPChallenge.DoesNotExist:
            raise ValidationError('OTP inválido')

        # Verificar intentos máximos
        if challenge.attempts >= cls.MAX_OTP_ATTEMPTS:
            challenge.status = 'BLOCKED'
            challenge.save()
            raise ValidationError('Máximo de intentos excedido. Genere un nuevo OTP.')

        # Verificar expiración
        if challenge.expires_at < timezone.now():
            challenge.status = 'EXPIRED'
            challenge.save()
            raise ValidationError('OTP expirado')

        # Verificar auth_id si se proporciona
        if auth_id and challenge.auth_id and challenge.auth_id != auth_id:
            raise ValidationError('Usuario no autorizado para este OTP')

        # Verificar código OTP
        if challenge.otp != otp:
            challenge.attempts = (challenge.attempts or 0) + 1
            challenge.status = 'ATTEMPTED'
            challenge.save()
            remaining = cls.MAX_OTP_ATTEMPTS - challenge.attempts
            raise ValidationError(f'OTP incorrecto. {remaining} intentos restantes.')

        # Marcar como usado si es correcto
        challenge.status = 'USED'
        challenge.save()

        LogTransferencia.objects.create(
            registro=payment_id,
            tipo_log='OTP',
            contenido=f'Challenge verificado: {challenge.challenge_id}'
        )

        return challenge 