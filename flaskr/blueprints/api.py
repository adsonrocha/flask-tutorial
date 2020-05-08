import datetime
from base64 import b64encode
from urllib.parse import urlencode

import jwt
import requests
from curlify import to_curl
from flask import Blueprint, request, jsonify, current_app

from flaskr.util.token_required import token_required
from flaskr.util.logger import Logger
from flaskr.util.logger import log_http_error

bp = Blueprint("api", __name__, url_prefix="/api")

json_content_type = 'application/json'
binary_content_type = 'application/octet-stream'

# TODO
base_login_uri = ''
token_uri = ''
api_uri = ''
CHUNK_SIZE = 5 * 1024 * 1024


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


def login_uri(client_id, scopes, redirect_uri):
    """
    Builds the URI for 'Log In with APP' link.
    The redirect_uri is a uri on client system (this app) that will handle the
    authorization once the user has authenticated with APP.
    """
    params = {
        'scope': scopes,
        'page': 'oidcauthn',
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri
    }
    return '{}?{}'.format(base_login_uri, urlencode(params))


def authorization_header(client_id, client_secret):
    """
    Builds the authorization header unique to each client.
    :param client_id: Provided by APP.
    :param client_secret: Provided by APP.
    :return: Basic authorization header.
    """
    pair = '{}:{}'.format(client_id, client_secret)
    encoded = b64encode(pair.encode('ascii')).decode('ascii')
    return 'Basic {}'.format(encoded)


def authorize(login_code, client_id, client_secret, redirect_uri):
    """
    Exchanges the login code provided on the redirect request for an
    access_token and refresh_token. Also gets user data.
    :param login_code: Authorization code returned from Log In with APP on redirect uri.
    :param client_id: Provided by APP.
    :param client_secret: Provided by APP.
    :param redirect_uri: Uri to your redirect page. Needs to be the same as
        the redirect uri provided in the initial Log In with APP request.
    :return: Object containing user data, access_token and refresh_token.
    """
    headers = {
        'authorization': authorization_header(client_id, client_secret),
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    data = {
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': login_code
    }
    res = requests.post(token_uri, headers=headers, data=urlencode(data))
    Logger().info(to_curl(res.request))
    if res.status_code == 200:
        return res.json()

    Logger().error("Auth failed: %s" % res.status_code)
    Logger().error("Auth failed: %s" % res.json())
    return None


def reauthorize(refresh_token, client_id, client_secret):
    """
    Access_tokens expire after 4 hours. At any point before the end of that
    period you may request a new access_token (and refresh_token) by submitting
    a POST request to the /api/oauth/token end-point. Note that the data
    submitted is slightly different than on initial authorization. Refresh
    tokens are good for 30 days from their date of issue. Once this end-point
    is called, the refresh token that is passed to this call is immediately set
    to expired one hour from "now" and the newly issues refresh token will
    expire 30 days from "now". Make sure to store the new refresh token so you
    can use it in the future to get a new auth tokens as needed. If you lose
    the refresh token there is no effective way to retrieve a new refresh token
    without having the user log in again.
    :param refresh_token: refresh_token supplied by initial (or subsequent refresh) call.
    :param client_id: Provided by Climate.
    :param client_secret: Provided by Climate.
    :return: Object containing user data, access_token and refresh_token.
    """
    headers = {
        'authorization': authorization_header(client_id, client_secret),
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    res = requests.post(token_uri, headers=headers, data=urlencode(data))
    Logger().info(to_curl(res.request))
    if res.status_code == 200:
        return res.json()

    log_http_error(res)
    return None


def bearer_token(token):
    """
    Returns content of authorization header to be provided on all non-auth
    API calls.
    :param token: access_token returned from authorization call.
    :return: Formatted header.
    """
    return 'Bearer {}'.format(token)
