from flask import Flask

# python uses this __name__ to identify if this is the main file of the application or if this is a module
app = Flask(__name__)

from app.controllers import default
