from flask_sqlalchemy import SQLAlchemy
from plugins.tunnel import set_global

DEFAULT_USER_PWD = 'ZhiMing123456'

db = SQLAlchemy()

set_global('db', db)

STATIC_FOLDER = 'plugin-static'
