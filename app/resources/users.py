from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from app.schemas.users import UserRegisterSchema, UserLoginSchema
from app.schemas.util import PostResponseSuccessSchema
from app.models.users import User, RevokedAccessTokens
from app import bcrypt

blp = Blueprint('Users', __name__, description='User related endpoints')


@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, user_data):
        username = user_data.get('username')
        password = user_data.get('password')
        email = user_data.get('email')
        phone_number = user_data.get('phone_number')

        if User.query.filter_by(username=username).first():
            abort(409, message=f'A user with {username} already exists.')

        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_pwd, phone_number=phone_number)
        user.save()

        return {'message': f'User successfully registered with username: {username}'}


@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = User.query.filter_by(username=user_data['username']).first()

        if user and bcrypt.check_password_hash(user.password, user_data['password']):
            identity = {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "phone_number": user.phone_number
                        }
            access_token = create_access_token(identity=identity, fresh=True)
            refresh_token = create_refresh_token(identity=identity)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 201

        abort(401, message='Invalid credentials.')


@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 201


@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    @blp.response(201, PostResponseSuccessSchema)
    def post(self):
        jti = get_jwt()["jti"]
        revoked_token = RevokedAccessTokens(jti=jti)
        revoked_token.save()
        return {'message': 'Access token has been revoked. User is logged out'}
