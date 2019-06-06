import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # Necesario para los formularios de Flask y evitar el CSRF.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bank.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
