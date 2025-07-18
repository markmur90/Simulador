import jwt
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime, timezone

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.EXEMPT_PATHS = [
            '/api/login/',
            '/api/token',
            '/oidc/token',
        ]

    def __call__(self, request):
        if not self._should_authenticate(request):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Token no proporcionado'}, status=401)

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=['HS256'],
                options={'verify_exp': True}
            )
            
            # Verificar expiración
            exp = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
            if exp < datetime.now(timezone.utc):
                return JsonResponse({'error': 'Token expirado'}, status=401)

            request.user_jwt = payload
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expirado'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Token inválido'}, status=401)

        return self.get_response(request)

    def _should_authenticate(self, request):
        # Solo autenticar peticiones a /api/ que no estén en EXEMPT_PATHS
        return (
            request.path.startswith('/api/') and 
            request.path not in self.EXEMPT_PATHS
        ) 