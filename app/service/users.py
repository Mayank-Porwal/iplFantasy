import smtplib
from random import randint

from flask_smorest import abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from app.models.users import RevokedAccessTokens
from app.models.otp import Otp
from app.dao.users import UserDAO
from app.dao.otp import OtpDAO
from app.service.email import CreateEmail


class UserService:
    def __init__(self) -> None:
        self.dao = UserDAO
        self.otp_dao = OtpDAO

    def register_user(self, dto) -> None:
        user = self.dao.get_user_by_email(dto['email'])
        if user:
            abort(409, message=f"A user with email {dto['email']} already exists.")

        dto['email'] = dto['email'].lower()
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

    def forgot_password(self, email: str) -> dict:
        user = self.dao.get_user_by_email(email)
        if not user:
            abort(404, message='Email not found')

        random_otp = randint(100000, 999999)
        otp_obj = self.otp_dao.get_otp_by_email(email)
        if otp_obj:
            return {'message': 'You already have an active OTP. Please check your mail.'}

        self.otp_dao.delete_otp(email)
        otp = Otp(email=email, otp=random_otp)
        otp.save()

        try:
            CreateEmail.send_email(email,
                                   subject='Forgot Password',
                                   text_content=f'OTP: {random_otp}. This is valid for next 10 minutes.')
            return {'message': f'Successfully sent password reset email to {email}'}
        except smtplib.SMTPException as e:
            return {'message': f'Failed with error: {e}'}

    def validate_otp(self, email: str, otp: int) -> int:
        user = self.dao.get_user_by_email(email)
        if not user:
            abort(404, message='Email not found')

        response = self.otp_dao.get_otp_by_email(email)
        if response:
            if response.otp == otp:
                self.otp_dao.delete_otp(email)
                return 1
            return 0
        return -1
