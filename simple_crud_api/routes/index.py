from importlib import import_module

from flask import (
    Blueprint,
    jsonify
)
from flask_mail import Message

simple_crud_api = import_module("simple_crud_api")

bp = Blueprint("index", __name__, url_prefix="/")

@bp.get("")
def hello():
    return jsonify(message="Hello to Flask API")
