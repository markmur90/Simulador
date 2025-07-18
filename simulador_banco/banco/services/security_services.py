import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import jwt
import pyotp

from banco.models import OTPChallenge, LogTransferencia

class SecurityService:
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 5
    JWT_ALGORITHM = 'HS256'
    MAX_OTP_ATTEMPTS = 3
    
    @classmethod
    def generate_jwt(cls, user_data: Dict, expiry_hours: int = 2) -> str:
        """
        Genera un token JWT válido.
        
        Args:
            user_data: Diccionario con datos del usuario
            expiry_hours: Horas hasta la expiración
            
        Returns:
            str: Token JWT firmado
        """
        payload = {
            **user_data,
            'exp': datetime.utcnow() + timedelta(hours=expiry_hours),
            'iat': datetime.utcnow(),
            'jti': secrets.token_hex(16)
        }
        
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=cls.JWT_ALGORITHM
        )

    @classmethod
    def verify_jwt(cls, token: str) -> Dict:
        """
        Verifica un token JWT y retorna su payload.
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Dict: Payload del token
            
        Raises:
            ValidationError: Si el token es inválido
        """
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[cls.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise ValidationError('Token expirado')
        except jwt.InvalidTokenError:
            raise ValidationError('Token inválido')

    @classmethod
    def generate_otp_challenge(
        cls,
        payment_id: str,
        auth_id: Optional[str] = None
    ) -> Tuple[OTPChallenge, str]:
        """
        Genera un nuevo desafío OTP.
        
        Args:
            payment_id: ID de la transferencia
            auth_id: ID del usuario autenticado
            
        Returns:
            Tuple[OTPChallenge, str]: Objeto challenge y código OTP
        """
        otp = ''.join(
            secrets.choice('0123456789') 
            for _ in range(cls.OTP_LENGTH)
        )
        
        challenge = OTPChallenge.objects.create(
            payment_id=payment_id,
            otp=otp,
            status='CREATED',
            auth_id=auth_id,
            expires_at=timezone.now() + timedelta(minutes=cls.OTP_EXPIRY_MINUTES)
        )
        
        LogTransferencia.objects.create(
            registro=payment_id,
            tipo_log='OTP',
            contenido=f'Challenge generado: {challenge.challenge_id}'
        )
        
        return challenge, otp

    @classmethod
    def verify_otp_challenge(
        cls,
        payment_id: str,
        otp: str,
        auth_id: Optional[str] = None
    ) -> OTPChallenge:
        """
        Verifica un desafío OTP con límite de intentos.
        
        Args:
            payment_id: ID de la transferencia
            otp: Código OTP a verificar
            auth_id: ID del usuario autenticado
            
        Returns:
            OTPChallenge: Objeto challenge verificado
            
        Raises:
            ValidationError: Si el OTP es inválido, expiró o excedió intentos
        """
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

    @staticmethod
    def generate_totp_secret() -> str:
        """Genera una nueva clave secreta para TOTP."""
        return pyotp.random_base32()

    @staticmethod
    def verify_totp(secret: str, code: str) -> bool:
        """
        Verifica un código TOTP.
        
        Args:
            secret: Clave secreta TOTP
            code: Código a verificar
            
        Returns:
            bool: True si el código es válido
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(code) 