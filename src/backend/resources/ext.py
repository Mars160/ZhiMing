import flask_restful as restful
from ext import db, DEFAULT_USER_PWD
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


def check_class_permission(uid: int, cid: int):
    role = User.getRoleByUid(uid)
    if role == '管理员':
        return True
    elif role == '教师':
        if db.session.query(RUC).filter(RUC.uid == uid, RUC.cid == cid).first():
            return True
    return False
