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