from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)

from .util import ListConverter

app.url_map.converters['list'] = ListConverter
app.config.from_object(Config)

from webapp import routes

def serve():
    Bootstrap(app)
    app.run()
