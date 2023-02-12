import flask_restful as restful
from ext import session
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import request

response_base = {
    "code": 0,
    "msg": "success",
    "data": None
}


def check_permission(uid: int, role: list):
    user = session.query(User).filter(User.id == uid).first()
    if user.role not in role:
        return False
    return True
