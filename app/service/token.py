from itsdangerous import URLSafeTimedSerializer
from app import run_app


def generate_token(email):
    serializer = URLSafeTimedSerializer(run_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=run_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(run_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=run_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
        return email
    except Exception:
        return False
