import os

from flask import Flask, render_template

from flaskr.blueprints import partner
from flaskr.util.logger import Logger
from flaskr.util.state import clear_state


# application factory function
def create_app(test_config=None):
    clear_state()

    # tells the app that configuration files are relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    logger = Logger(app.logger)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html', error=error), 404

    # register the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the flaskr
    from .blueprints import auth, blog, api, partner

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(partner.bp)

    # make url_for('index') == url_for('partner.index')
    app.add_url_rule("/partner/", endpoint="index")

    return app
