from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.schemas.users import UserRegisterSchema, UserLoginSchema
from app.schemas.util import PostResponseSuccessSchema
from app.models.users import User, RevokedAccessTokens
from app import bcrypt, create_app
from app.service.token import generate_token, confirm_token

blp = Blueprint('Confirm Email', __name__, description='Confirmation mail related endpoints')


@blp.route('/confirm-email/<str: token>')
class ConfirmEmail(MethodView):
    def get(self, token):
        email = confirm_token(token)
        




