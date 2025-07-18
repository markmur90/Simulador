import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import qrcode
import io
import base64
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import jwt
import pyotp
from jose import JWTError, jwt as jose_jwt

from banco.models import OTPChallenge, LogTransferencia, OficialBancario

class SecurityService:
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 5
    JWT_ALGORITHM = 'HS256'
    MAX_OTP_ATTEMPTS = 3
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    @classmethod
    def generate_token_pair(cls, user_data: Dict) -> Dict[str, str]:
        """
        Genera un par de tokens JWT (access + refresh).
        
        Args:
            user_data: Diccionario con datos del usuario
            
        Returns:
            Dict con access_token y refresh_token
        """
        # Access token con vida corta
        access_payload = {
            **user_data,
            'exp': datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        # Refresh token con vida larga
        refresh_payload = {
            'user_id': user_data.get('id'),
            'exp': datetime.utcnow() + timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS),
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        
        access_token = jose_jwt.encode(
            access_payload,
            settings.JWT_SECRET_KEY,
            algorithm=cls.JWT_ALGORITHM
        )
        
        refresh_token = jose_jwt.encode(
            refresh_payload,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithm=cls.JWT_ALGORITHM
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer'
        }

    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> str:
        """
        Genera un nuevo access token usando un refresh token válido.
        
        Args:
            refresh_token: Token de refresco
            
        Returns:
            str: Nuevo access token
            
        Raises:
            ValidationError: Si el refresh token es inválido
        """
        try:
            payload = jose_jwt.decode(
                refresh_token,
                settings.JWT_REFRESH_SECRET_KEY,
                algorithms=[cls.JWT_ALGORITHM]
            )
            
            if payload.get('type') != 'refresh':
                raise ValidationError('Token tipo inválido')
                
            user = OficialBancario.objects.get(id=payload.get('user_id'))
            
            return cls.generate_token_pair({
                'id': user.id,
                'username': user.username,
                'role': user.role
            })['access_token']
            
        except (JWTError, OficialBancario.DoesNotExist):
            raise ValidationError('Refresh token inválido')

    @classmethod
    def setup_totp(cls, user: OficialBancario) -> Tuple[str, str]:
        """
        Configura TOTP para un usuario.
        
        Args:
            user: Usuario para configurar TOTP
            
        Returns:
            Tuple[str, str]: (secret_key, qr_code_base64)
        """
        # Generar secreto TOTP
        secret = pyotp.random_base32()
        
        # Crear URI para QR
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            user.username,
            issuer_name="Simulador Bancario"
        )
        
        # Generar QR
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        # Convertir QR a base64
        img_buffer = io.BytesIO()
        qr.make_image(fill_color="black", back_color="white").save(img_buffer, format='PNG')
        qr_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return secret, qr_base64

    @classmethod
    def verify_totp(cls, secret: str, code: str) -> bool:
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