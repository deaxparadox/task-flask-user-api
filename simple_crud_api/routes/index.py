from flask import (
    Blueprint,
    jsonify
)

bp = Blueprint("index", __name__, url_prefix="/")

@bp.get("")
def hello():
    return jsonify(message="Hello to Flask API")
