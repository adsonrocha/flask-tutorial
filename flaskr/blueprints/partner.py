from flask import Blueprint, render_template, url_for

from flaskr.blueprints import api
from flaskr.util.state import state

bp = Blueprint("partner", __name__)

# Configuration of the REST API credentials
PARTNER_ID = ""  # os.environ['PARTNER_ID']  # OAuth2 client ID
PARTNER_SECRET = ""  # os.environ['PARTNER_SECRET']  # OAuth2 client secret
PARTNER_SCOPES = ""  # os.environ['PARTNER_SCOPES']  # Oauth2 scope list
PARTNER_KEY = ""  # os.environ['PARTNER_KEY']  # X-Api-Key header


# Partner app server
@bp.route('/')
def index():
    if state('user'):
        return user_home()
    return no_user()


def user_home():
    return render_template("partner/home.html", access_token="", refresh_token="", refresh_token_url="")


def no_user():
    """
    Page where you present a link to Log in with REST API.
    :return: None
    """
    login_uri = api.login_uri(PARTNER_ID, PARTNER_SCOPES, redirect_uri())
    return render_template("partner/no_user.html", login_uri=login_uri)


def redirect_uri():
    """
    :return: Returns uri for redirection after Log In with REST API.
    """
    return url_for('login_redirect', _external=True)
