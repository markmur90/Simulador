import os
import pyotp
import qrcode

def get_totp_secret() -> str:
    """Return the TOTP secret stored in env or create one."""
    secret = os.environ.get("TOTP_SECRET")
    if not secret:
        secret = pyotp.random_base32()
        os.environ["TOTP_SECRET"] = secret
    return secret

def verify_totp(code: str) -> bool:
    """Verify a TOTP code using the shared secret."""
    try:
        totp = pyotp.TOTP(get_totp_secret())
        return totp.verify(code)
    except Exception:
        return False

def generate_totp_qr(user: str) -> str:
    """Generate a QR code for the TOTP secret and return its path."""
    totp = pyotp.TOTP(get_totp_secret())
    uri = totp.provisioning_uri(name=user, issuer_name="BancoSeguro")
    img = qrcode.make(uri)
    path = f"/tmp/{user}_totp.png"
    img.save(path)
    return path