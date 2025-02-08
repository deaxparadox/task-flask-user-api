import os
from datetime import timedelta
from flask import (
    Flask, g, 
    redirect, url_for, 
    render_template, session
)
from flask_jwt_extended import JWTManager
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

from . import settings
from .models.user import User
from .routes import auth_user, auth, index
from .database import db_session, init_db
from . import settings


# app factory function
def create_app(test_config=None):
    # creat and configure the app
    app = Flask(
        __name__, 
        instance_relative_config=True
    )
    app.config.from_mapping(
        SECRET_KEY=settings.SECRET_KEY
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config it passed in
        app.config.from_mapping(test_config)
        
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        minutes=int(settings.JWT_ACCESS_TOKEN_EXPIRES)
    )
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(
        days=int(settings.JWT_REFRESH_TOKEN_EXPIRES)
    )
    jwt = JWTManager(app)
    
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user.id)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return db_session.query(User).filter_by(id=identity).one_or_none()

    app.register_blueprint(index.bp)
    app.register_blueprint(auth_user.bp)
    app.register_blueprint(auth.bp)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app