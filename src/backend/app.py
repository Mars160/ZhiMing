from flask import Flask
from flask_jwt_extended import JWTManager
from os import urandom
from resources import api
from ext import db
from dbconfig import MYSQL_STRING


app = Flask(__name__)
if app.config['ENV'] == 'development':
    app.config['JWT_SECRET_KEY'] = 'secret'
else:
    app.config['JWT_SECRET_KEY'] = urandom(64)
    app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_STRING
jwt = JWTManager(app)
api.init_app(app)
db.init_app(app)

from migrate import *


if __name__ == '__main__':
    app.run()
