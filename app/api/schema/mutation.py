from ariadne import MutationType
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.auth.decorators import login_required

mutation = MutationType()

@mutation.field("register")
def resolve_register(_, info, username, email, password):
    print(f"Register Mutation Called: {username}, {email}")
    response =  AuthService.register_user(username, email, password)
    print("Register Response:", response)
    return response

@mutation.field("login")
def resolve_login(_, info, email, password):
    return AuthService.login_user(email, password)

@mutation.field("refreshToken")
@jwt_required(refresh=True)
def resolve_refresh_token(_, info):
    user_id = get_jwt_identity()
    return AuthService.refresh_token(user_id)

@mutation.field("logout")
@login_required
def resolve_logout(_, info):
    return AuthService.logout_user()