from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import jwt, redis_client

def add_token_to_blocklist(jti, expires_delta):
    redis_client.setex(f'jwt_blocklist:{jti}', int(expires_delta.total_seconds()), '1')

def is_token_revoked(jwt_payload):
    jti = jwt_payload['jti']
    token_in_redis = redis_client.get(f'jwt_blocklist:{jti}')
    return token_in_redis is not None

def generate_tokens(user_id):
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    return access_token, refresh_token

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return is_token_revoked(jwt_payload)