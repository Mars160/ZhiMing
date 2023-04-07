from flask import Flask
from flask_jwt_extended import JWTManager
import os
from resources import api
from ext import db
from dbconfig import MYSQL_STRING
import logging
from time import sleep
from plugins.tunnel import set_global
import shutil
import atexit

DEBUG = True
STATIC_FOLDER = 'plugin-static'

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('DEBUG模式已开启')
else:
    logging.basicConfig(level=logging.INFO)

logging.info('服务启动中')
app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/plugin')
set_global('app', app)
app.config['JSON_AS_ASCII'] = False
if DEBUG:
    app.config['JWT_SECRET_KEY'] = 'secret'
else:
    app.config['JWT_SECRET_KEY'] = os.urandom(64)
    app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_STRING
jwt = JWTManager(app)
set_global('jwt', jwt)

logging.info('3s后清空static目录...')
if not DEBUG:
    sleep(3)

for file in os.listdir(STATIC_FOLDER):
    if file != 'DO NOT PUT FILES HERE' or file != 'README.md':
        os.remove(os.path.join(STATIC_FOLDER, file))

logging.info('复制加载plugin中的静态资源')
for plugin in os.listdir('plugins'):
    if os.path.isdir(os.path.join('plugins', plugin)):
        os.mkdir(STATIC_FOLDER + os.sep + plugin)
        if os.path.isdir(os.path.join('plugins', plugin, "static")):
            for file in os.listdir(os.path.join('plugins', plugin, "static")):
                shutil.copy(os.path.join('plugins', plugin, "static", file),
                            STATIC_FOLDER + os.sep + plugin + os.sep + file)


@atexit.register
def clean():
    logging.info('程序结束，清空static目录')
    for file in os.listdir(STATIC_FOLDER):
        if file != 'DO NOT PUT FILES HERE' or file != 'README.md':
            shutil.rmtree(os.path.join(STATIC_FOLDER, file))


api.init_app(app)
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=DEBUG)
