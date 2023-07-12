from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from app.models import User, RevokedAccessTokens
from app import db, bcrypt

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    username = payload.get('username')
    password = payload.get('password')
    email = payload.get('email')
    phone_number = payload.get('phone_number')

    if User.query.filter_by(username=username).first():
        return {'message': f'A user with {username} already exists.'}, 409

    hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_pwd, phone_number=phone_number)

    db.session.add(user)
    db.session.commit()

    return {'message': f'User successfully registered with username: {username}'}, 201


@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    username = payload.get('username')
    password = payload.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        identity = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number
        }
        access_token = create_access_token(identity=identity, fresh=True)
        refresh_token = create_refresh_token(identity=identity)
        return {'access_token': access_token, 'refresh_token': refresh_token}, 201
    return {'message': 'Invalid credentials'}, 401


@users.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    revoked_token = RevokedAccessTokens(jti=jti)
    revoked_token.save()
    return {'message': 'Access token has been revoked. User is logged out'}, 201


@users.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    return {'access_token': new_token}, 201



# @users.route('/account', methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)
#             current_user.image_file = picture_file
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Your Account has been updated.', 'success')
#         return redirect(url_for('users.account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#
#     image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
#     return render_template('account.html', title='Account', image_file=image_file, form=form)
