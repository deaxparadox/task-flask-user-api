from flask import (
    Blueprint,
    redirect,
    render_template,
    session,
    url_for, jsonify
)

bp = Blueprint("index", __name__, url_prefix="/")

@bp.get("")
def hello():
    # return jsonify({
    #     "message": "Hello Flask API"
    # })
    return jsonify(message="Hello to Flask API")
