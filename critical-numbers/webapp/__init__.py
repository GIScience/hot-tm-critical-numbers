from flask import Flask
from config import Config

app = Flask(__name__)

from .util import ListConverter
from flask_bootstrap import Bootstrap


app.url_map.converters['list'] = ListConverter
app.config.from_object(Config)
bootstrap = Bootstrap(app)


from webapp import routes


def serve():
    app.run()
