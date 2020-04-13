from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# python uses this __name__ to identify if this is the main file of the application or if this is a module
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app.controllers import default
