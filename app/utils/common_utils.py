import uuid
from flask_smorest import abort
from flask_jwt_extended import get_jwt_identity


def generate_uuid() -> str:
    return uuid.uuid4().hex[:5].upper()


def fetch_user_from_jwt() -> str | dict:
    email = get_jwt_identity().get('email')
    if not email:
        abort(498, message='invalid token')
    return email
