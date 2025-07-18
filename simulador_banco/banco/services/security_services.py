import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import jwt
import pyotp

from banco.models import OTPChallenge, LogTransferencia, OficialBancario

class SecurityService:
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 5
    JWT_ALGORITHM = 'HS256'
    MAX_OTP_ATTEMPTS = 3
    
    @classmethod
    def authenticate_oficial(cls, username: str, password: str) -> Optional[OficialBancario]:
        """Autentica un oficial bancario y retorna el objeto si es válido."""
        try:
            oficial = OficialBancario.objects.get(username=username)
            if oficial.check_password(password):
                return oficial
        except OficialBancario.DoesNotExist:
            pass
        return None
    
    @classmethod
    def generate_jwt(cls, user_data: Dict, expiry_hours: int = 2) -> str:
        """Genera un token JWT válido."""
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
        """Verifica un token JWT y retorna su payload."""
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
    def generate_otp_challenge(cls, payment_id: str, username: str) -> Tuple[OTPChallenge, str]:
        """Genera un nuevo desafío OTP para una transferencia."""
        otp = ''.join(secrets.choice('0123456789') for _ in range(cls.OTP_LENGTH))
        
        challenge = OTPChallenge.objects.create(
            challenge_id=secrets.token_hex(16),
            payment_id=payment_id,
            otp_hash=cls.hash_otp(otp),
            username=username,
            expires_at=timezone.now() + timedelta(minutes=cls.OTP_EXPIRY_MINUTES)
        )
        
        return challenge, otp

    @classmethod
    def hash_otp(cls, otp: str) -> str:
        """Genera un hash seguro del OTP."""
        return secrets.token_hex(32)  # Simplificado para el ejemplo

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

import os
import logging
import requests
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import qrcode

logger = logging.getLogger('banco.telegram')

class TelegramService:
    """Servicio para enviar notificaciones por Telegram con imágenes."""
    
    @staticmethod
    def send_notification(message, image_path=None):
        """
        Envía una notificación por Telegram, opcionalmente con una imagen.
        
        Args:
            message (str): Mensaje a enviar
            image_path (str, optional): Ruta a la imagen a adjuntar
        """
        try:
            bot_token = settings.TELEGRAM_BOT_TOKEN
            chat_id = settings.TELEGRAM_CHAT_ID
            
            if not bot_token or not chat_id:
                logger.warning("Telegram no configurado - saltando notificación")
                return
                
            # Agregar emojis según el tipo de mensaje
            if "transferencia" in message.lower():
                message = "💸 " + message
            elif "error" in message.lower():
                message = "❌ " + message
            elif "login" in message.lower():
                message = "🔐 " + message
            elif "otp" in message.lower():
                message = "🔑 " + message
            
            # Enviar mensaje
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            # Si hay imagen, enviarla
            if image_path:
                url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
                files = {
                    "photo": open(image_path, "rb")
                }
                data = {
                    "chat_id": chat_id,
                    "caption": "📎 Imagen adjunta al mensaje anterior"
                }
                response = requests.post(url, data=data, files=files)
                response.raise_for_status()
                
            logger.info(f"Notificación enviada: {message}")
            
        except Exception as e:
            logger.error(f"Error enviando notificación: {str(e)}")
            
    @staticmethod
    def create_transfer_image(transfer):
        """
        Crea una imagen con los detalles de la transferencia.
        
        Args:
            transfer (Transfer): Objeto de transferencia
            
        Returns:
            str: Ruta al archivo de imagen temporal
        """
        try:
            # Crear imagen
            img = Image.new('RGB', (600, 400), color='white')
            d = ImageDraw.Draw(img)
            
            # Cargar fuente (usar una por defecto si no está disponible)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
            except:
                font = ImageFont.load_default()
                
            # Dibujar detalles
            d.text((20, 20), "Detalles de Transferencia", font=font, fill='black')
            d.text((20, 60), f"De: {transfer.debtor.name}", font=font, fill='black')
            d.text((20, 100), f"A: {transfer.creditor.name}", font=font, fill='black')
            d.text((20, 140), f"Monto: {transfer.instructed_amount} {transfer.currency}", font=font, fill='black')
            d.text((20, 180), f"Estado: {transfer.status}", font=font, fill='black')
            d.text((20, 220), f"ID: {transfer.payment_id}", font=font, fill='black')
            
            # Guardar temporalmente
            temp_path = f"/tmp/transfer_{transfer.payment_id}.png"
            img.save(temp_path)
            
            return temp_path
            
        except Exception as e:
            logger.error(f"Error creando imagen: {str(e)}")
            return None
            
    @staticmethod
    def create_qr_code(data, title=""):
        """
        Crea un código QR con un título opcional.
        
        Args:
            data (str): Datos para el código QR
            title (str): Título opcional sobre el QR
            
        Returns:
            str: Ruta al archivo QR temporal
        """
        try:
            # Crear QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Crear imagen con espacio para título
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            if title:
                # Crear imagen más grande para incluir título
                img = Image.new('RGB', (qr_img.size[0], qr_img.size[1] + 40), 'white')
                d = ImageDraw.Draw(img)
                
                # Agregar título
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
                except:
                    font = ImageFont.load_default()
                    
                d.text((10, 10), title, font=font, fill='black')
                
                # Pegar QR
                img.paste(qr_img, (0, 40))
                qr_img = img
                
            # Guardar temporalmente
            temp_path = f"/tmp/qr_{hash(data)}.png"
            qr_img.save(temp_path)
            
            return temp_path
            
        except Exception as e:
            logger.error(f"Error creando QR: {str(e)}")
            return None 