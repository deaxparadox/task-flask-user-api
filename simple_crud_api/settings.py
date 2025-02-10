import os
from flask_jwt_extended import JWTManager

SECRET_KEY = os.environ.get("SECRET_KEY")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
DBNAME = os.environ.get("DBNAME")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

DATABASE_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

ENCODING = os.environ.get("ENCODING")

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = os.environ.get("JWT_ACCESS_TOKEN_EXPIRES")
JWT_REFRESH_TOKEN_EXPIRES = os.environ.get("JWT_REFRESH_TOKEN_EXPIRES")

MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("TEST_APP")
MAIL_USE_TLS = False
MAIL_TLS_PORT = os.environ.get('MAIL_TLS_PORT')
MAIL_USE_SSL = True
MAIL_SSL_PORT = os.environ.get('MAIL_SSL_PORT')
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")

CACHE_TYPE = os.environ.get('CACHE_TYPE')
CACHE_DEFAULT_TIMEOUT = os.environ.get('CACHE_DEFAULT_TIMEOUT')
CACHE_DIR = os.environ.get('CACHE_DIR')