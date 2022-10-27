from itsdangerous import URLSafeTimedSerializer
from flask_app.config import Config


def generate_verification_token(email):
    """Generates token based on user secret key"""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)


def verify_token(token, expiration=3600):
    """Maintains verification link and forwards response"""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=Config.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email
