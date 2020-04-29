import functools
import datetime
import jwt

from flask import Blueprint, g, request, jsonify, current_app, redirect, url_for
from werkzeug.exceptions import abort

bp = Blueprint("api", __name__, url_prefix="/api")


def token_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({
                "error": "Unauthorized"
            }), 403

        if "Bearer" not in token:
            return jsonify({
                "error": "Invalid token"
            }), 401

        try:
            token_pure = token.replace("Bearer", "")
            options = {
                'verify_signature': False,
                'verify_exp': True,
                'verify_nbf': False,
                'verify_iat': True,
                'verify_aud': False
            }
            decoded = jwt.decode(token_pure, current_app.config["SECRET_KEY"], algorithms=['HS256'], options=options)
            print(decoded["id"])
        except ValueError as e:
            return jsonify({
                "error": "invalid id"
            })

        return view(**kwargs)

    return wrapped_view


@bp.route("/test/<int:id>", methods=("GET", "POST"))
def test(id):
    if request.method == "GET":
        payload = {
            "id": id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], 'HS256').decode('utf-8')
        # print(token)
        return jsonify({
            "token": token
        }), 200
    else:
        params = request.json["params"]
        return jsonify({
            "message": "POST",
            "params": params
        }), 201


@bp.route("/protected", methods=["GET"])
@token_required
def protected():
    return jsonify({
        "message": "SUCCESS",
    }), 200
