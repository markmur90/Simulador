from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
import re

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.RATE_LIMIT = getattr(settings, 'API_RATE_LIMIT', 100)  # requests per minute
        self.SANITIZE_PATTERNS = [
            (r'<[^>]*>', ''),  # Remove HTML tags
            (r'javascript:', ''),  # Remove javascript: protocol
            (r'data:', ''),  # Remove data: protocol
            (r'(\s|\'|\"|%22|%27)*((on\w+)|\w+:)(\s|\'|\"|%22|%27)*=', '')  # Remove event handlers
        ]

    def __call__(self, request):
        if request.path.startswith('/api/'):
            # Rate limiting
            client_ip = self._get_client_ip(request)
            if not self._check_rate_limit(client_ip):
                return JsonResponse({'error': 'Rate limit exceeded'}, status=429)

            # Input sanitization for JSON data
            if request.content_type == 'application/json' and request.body:
                try:
                    sanitized_body = self._sanitize_data(request.body.decode('utf-8'))
                    request._body = sanitized_body.encode('utf-8')
                except Exception:
                    return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        response = self.get_response(request)

        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = "default-src 'self'"

        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def _check_rate_limit(self, client_ip):
        cache_key = f'rate_limit_{client_ip}'
        try:
            rate = cache.get(cache_key, 0)
            if rate >= self.RATE_LIMIT:
                return False
            cache.set(cache_key, rate + 1, 60)  # 1 minute expiry
            return True
        except Exception:
            return True  # Default to allowing if cache fails

    def _sanitize_data(self, data):
        if isinstance(data, str):
            for pattern, replacement in self.SANITIZE_PATTERNS:
                data = re.sub(pattern, replacement, data, flags=re.IGNORECASE)
            return data
        return data 