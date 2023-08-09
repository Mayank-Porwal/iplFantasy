from flask_smorest import abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from app.models.users import RevokedAccessTokens
from app.dao.users import UserDAO


class UserService:
    def __init__(self) -> None:
        self.dao = UserDAO

    def register_user(self, dto) -> None:
        user = self.dao.get_user_by_email(dto['email'])
        if user:
            abort(409, message=f"A user with email {dto['email']} already exists.")

        self.dao.add_user(dto)

    def login_user(self, dto) -> dict:
        user = self.dao.get_user_by_email(dto['email'])

        if user and self.dao.check_password(user.password, dto['password']):
            identity = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone_number": user.phone_number
            }
            access_token = create_access_token(identity=identity, fresh=True)
            refresh_token = create_refresh_token(identity=identity)
            return {'access_token': access_token, 'refresh_token': refresh_token}

        abort(401, message='Invalid credentials.')

    @staticmethod
    def refresh() -> dict:
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}

    @staticmethod
    def logout() -> dict:
        jti = get_jwt()["jti"]
        revoked_token = RevokedAccessTokens(jti=jti)
        revoked_token.save()
        return {'message': 'Access token has been revoked. User is logged out'}
