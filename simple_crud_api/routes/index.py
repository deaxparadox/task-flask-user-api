from importlib import import_module

from flask import (
    Blueprint,
    jsonify
)

from ..cache import cache


bp = Blueprint("index", __name__, url_prefix="/")

@bp.get("")
def hello():
    return jsonify(message="Hello to Flask API")
