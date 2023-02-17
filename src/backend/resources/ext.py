import flask_restful as restful
from ext import db
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

response_base = {
    "code": 0,
    "msg": "success",
    "data": None
}


def check_permission(uid: int, roles: list):
    role = User.getRoleByUid(uid)
    if role not in roles:
        return False
    return True
