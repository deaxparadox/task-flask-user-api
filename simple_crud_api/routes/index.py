from importlib import import_module

from flask import (
    Blueprint,
    jsonify
)


bp = Blueprint("index", __name__, url_prefix="/")


@bp.get("")
def hello():
    return jsonify(message="Hello to Flask API")


@bp.cli.command("hello")
def hello():
    print("hello to every one")
    