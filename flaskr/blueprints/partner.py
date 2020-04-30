import os

from flask import Blueprint, render_template, url_for

from flaskr.blueprints import api
from flaskr.util.state import state

bp = Blueprint("partner", __name__, url_prefix="/partner")

# Configuration of your APP partner credentials. This assumes you have
# placed them in your environment.

APP_API_ID = ""  # os.environ['APP_API_ID']  # OAuth2 client ID
APP_API_SECRET = ""  # os.environ['APP_API_SECRET']  # OAuth2 client secret
APP_API_SCOPES = ""  # os.environ['APP_API_SCOPES']  # Oauth2 scope list
APP_API_KEY = ""  # os.environ['APP_API_KEY']  # X-Api-Key header


# Partner app server
@bp.route('/')
def index():
    if state('user'):
        return user_home()
    return no_user()


def user_home():
    return render_template("partner/home.html",
                           access_token="",
                           refresh_token="",
                           refresh_token_url=""
                           )


def no_user():
    """
    Page where you present a link to Log In with APP.
    :return: None
    """
    login_uri = api.login_uri(APP_API_ID, APP_API_SCOPES, redirect_uri())
    return render_template("partner/no_user.html", login_uri=login_uri)


def redirect_uri():
    """
    :return: Returns uri for redirection after Log In with APP.
    """
    return url_for('login_redirect', _external=True)
