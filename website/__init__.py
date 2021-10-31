from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import configparser


db = SQLAlchemy()
config_parser = configparser.ConfigParser()


def create_app():
    config_parser.read('creds.ini')
    username = config_parser['Database']['username']
    password = config_parser['Database']['password']
    endpoint = config_parser['Database']['endpoint']
    database = config_parser['Database']['database']
    secret_key = config_parser['Server']['secret_key']
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s' % (username, password, endpoint, database)
    db.init_app(app)

    from .views import views
    from . import rest_api

    app.register_blueprint(views, url_prefix='/')
    api = Api(app)
    rest_api.add_resources(api)

    return app

