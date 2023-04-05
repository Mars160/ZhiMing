from flask import Flask
from flask_jwt_extended import JWTManager
from os import urandom
from resources import api
from ext import db
from dbconfig import MYSQL_STRING
import click

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


@app.cli.command('create-db')
def create_db():
    db.create_all()
    click.echo('数据库创建成功')


@app.cli.command('drop-db')
def drop_db():
    db.drop_all()
    click.echo('数据库删除成功')


@app.cli.command('create-admin')
@click.argument('name', default='admin')
@click.argument('pwd', default='admin')
def create_admin(name, pwd):
    from models import User
    admin = User()
    admin.uid = 0
    admin.uname = name
    admin.role = '管理员'
    admin.nickname = '管理员'
    admin.setPassword(pwd)
    db.session.add(admin)
    db.session.commit()
    click.echo('管理员账号创建成功')


if __name__ == '__main__':
    app.run()
