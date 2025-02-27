from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate, jwt, init_redis
from app.config import config_by_name


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():
        init_redis(app)

        from app.api.routes import init_app as init_api_routes
        init_api_routes(app)

        db.create_all()
    
    return app

