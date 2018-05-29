# Code taken from: https://explore-flask.readthedocs.io/en/latest/views.html
# Specify part of the URL to be converted into Python List of Integer

from werkzeug.routing import BaseConverter

class ListConverter(BaseConverter):

    def to_python(self, value):
        return list(map(int, value.split('+')))

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value)
                        for value in values)
