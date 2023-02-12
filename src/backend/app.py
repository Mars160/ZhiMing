from flask import Flask
from flask_jwt_extended import JWTManager
from random import randbytes
from resources import api

app = Flask(__name__)
if app.config['ENV'] == 'development':
    app.config['JWT_SECRET_KEY'] = 'secret'
else:
    app.config['JWT_SECRET_KEY'] = randbytes(64)
jwt = JWTManager(app)
api.init_app(app)

if __name__ == '__main__':
    app.run()
