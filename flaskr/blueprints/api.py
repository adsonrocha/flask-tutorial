import functools
import datetime
import jwt

from flask import Blueprint, g, request, jsonify
from werkzeug.exceptions import abort

bp = Blueprint("api", __name__, url_prefix="/api")


def token_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.token is None:
            abort(403)

        return view(**kwargs)

    return wrapped_view


@bp.route("/test", methods=("GET", "POST"))
# @token_required
def test():
    if request.method == "POST":
        token = request.json["token"]

        payload = {
            "id": "123",
            "exp": datetime.datetime.utcnow()
        }

        return jsonify({
            "message": token
        }), 200
    else:
        return jsonify({
            "message": "GET"
        }), 201
