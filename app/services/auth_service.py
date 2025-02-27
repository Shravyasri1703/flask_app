from flask import current_app
from flask_jwt_extended import get_jwt
from datetime import datetime, timezone
from app.models.user import User
from app.extensions import db
from app.auth.jwt import generate_tokens, add_token_to_blocklist

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return {
                'success': False,
                'message': 'Username or email Already exists'
            }
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        access_token, refresh_token = generate_tokens(user.id)

        return {
            'success': True,
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return {
                'success': False,
                'message': 'Invalid credentials'
            }

        access_token, refresh_token = generate_tokens(user.id)

        return {
            'success': True,
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    @staticmethod
    def refresh_token(user_id):
        user = User.query.get(user_id)
        if not user:
            return {
                'success': False,
                'message' : 'user not found'
            }
        
        access_token = generate_tokens(user.id)[0]

        return {
            'success': True,
            'access_token': access_token
        }
    
    @staticmethod
    def logout_user():
        jwt_payload = get_jwt()
        jti = jwt_payload['jti']
        exp = jwt_payload['exp']
        expires_delta = datetime.fromtimestamp(exp, tz=timezone.utc) - datetime.now(timezone.utc)

        add_token_to_blocklist(jti, expires_delta)

        return {
            'success': True,
            'message': 'Successfully logged out'
        }