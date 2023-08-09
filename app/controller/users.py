from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from app.schemas.users import UserRegisterSchema, UserLoginSchema
from app.schemas.util import PostResponseSuccessSchema
from app.service.users import UserService

blp = Blueprint('Users', __name__, description='User related endpoints')
service = UserService()


@blp.route('/register')
class UserRegister(MethodView):
    @cross_origin()
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, PostResponseSuccessSchema)
    def post(self, user_data: dict):
        service.register_user(user_data)
        return {'message': f"User successfully registered with email: {user_data['email']}"}


@blp.route('/login')
class UserLogin(MethodView):
    @cross_origin()
    @blp.arguments(UserLoginSchema)
    def post(self, user_data: dict):
        return service.login_user(user_data), 201


@blp.route('/refresh')
class TokenRefresh(MethodView):
    @cross_origin()
    @jwt_required(refresh=True)
    def post(self):
        return UserService.refresh(), 201


@blp.route('/logout')
class UserLogout(MethodView):
    @cross_origin()
    @jwt_required()
    @blp.response(201, PostResponseSuccessSchema)
    def post(self):
        return UserService.logout()
