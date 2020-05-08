import functools

import jwt
from flask import request, jsonify, current_app


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
