from app.models.users import User
from app import bcrypt


class UserDAO:
    @staticmethod
    def get_user_by_email(email: str) -> User:
        user: User = User.query.filter_by(email=email).first()
        return user if user else {}

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        user: User = User.query.filter_by(id=user_id).first()
        return user if user else {}

    @staticmethod
    def add_user(user_data: dict) -> None:
        hashed_pwd = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user_data['password'] = hashed_pwd
        user = User(**user_data)
        user.save()

    @staticmethod
    def check_password(stored_pwd: str, request_pwd: str) -> bool:
        return bcrypt.check_password_hash(stored_pwd, request_pwd)
