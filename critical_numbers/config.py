import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SERVER_NAME = 'disastertools.heigit.org/critical_numbers/'
