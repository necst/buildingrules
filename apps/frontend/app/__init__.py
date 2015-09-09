from flask import Flask

app = Flask(__name__)
from app.gui import gui

app.register_blueprint(gui)
