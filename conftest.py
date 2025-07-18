import os
import sys
from pathlib import Path

# Minimal environment variables for Django settings
os.environ.setdefault('FIELD_ENCRYPTION_KEY', 'DbQG9CWLvBRa8Iu9pv9fJDVURCdKYQQErlZ9oCYGsY8=')
os.environ.setdefault('SECRET_KEY', 'secret')
os.environ.setdefault('JWT_SECRET_KEY', 'jwt')

os.environ.setdefault('BASE_URL', 'http://80.78.30.242:9181')
os.environ.setdefault('TOKEN_PATH', '/oidc/token')
os.environ.setdefault('AUTHORIZE_PATH', '/oidc/authorize')
os.environ.setdefault('OTP_PATH', '/otp/single')
os.environ.setdefault('AUTH_PATH', '/auth/challenges')
os.environ.setdefault('API_PATH', '/payments')
os.environ.setdefault('SIMULATOR_NOTIFY_URL', 'http://localhost/notify')
os.environ.setdefault('TOTP_SECRET', 'JBSWY3DPEHPK3PXP')