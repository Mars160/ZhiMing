from .ext import *


class Users(restful.Resource):
    @jwt_required()
    def get(self):
        response = response_base.copy()

        cur_uid = get_jwt_identity()

        limit = request.args.get('limit', 10, type=int)
        page = request.args.get('page', 1, type=int)

        role = User.getRoleByUid(cur_uid)
        if role == '管理员':
            users = db.session.query(User).filter(User.role == '教师').limit(limit).offset((page - 1) * limit).all()
            response['data'] = [{'uid': user.uid, 'uname': user.uname, 'role': user.role} for user in users]
        elif role == '教师':
            users = db.session.query(User).filter(User.role == '学生').limit(limit).offset((page - 1) * limit).all()
            response['data'] = [{'uid': user.uid, 'uname': user.uname, 'role': user.role} for user in users]
        else:
            response['code'] = 403
            response['msg'] = 'permission denied'
        return response

    @jwt_required()
    def post(self):
        response = response_base.copy()
        cur_uid = get_jwt_identity()

        data = request.get_json()

        role = User.getRoleByUid(cur_uid)

        uid = None
        if 'uid' in data:
            uid = data['uid']
        uname = data['uname']
        urole = None
        if 'role' in data:
            role = data['role']

        if role == '管理员':
            if urole is None:
                urole = '教师'
        elif role == '教师':
            urole = '学生'
        else:
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        user = db.session.query(User).filter(User.uid == uid).first()
        if user is not None:
            response['code'] = 400
            response['msg'] = 'user already exists'
            return response
        else:
            user = User()
            # user.uid = uid
            user.uname = uname
            user.role = urole
            user.setPassword(None)
            db.session.add(user)
            db.session.commit()
            response['data'] = user.uid
            return response

    @jwt_required()
    def put(self, uid: int):
        response = response_base.copy()
        cur_uid = get_jwt_identity()

        data = request.get_json()

        role = User.getRoleByUid(cur_uid)

        user = db.session.query(User).filter(User.uid == uid).first()

        if role == '管理员':
            if 'uname' in data:
                user.uname = data['uname']
            if 'role' in data:
                user.role = data['role']
            if 'pwd' in data:
                user.setPassword(data['pwd'])
            db.session.commit()
            return response
        elif role == '教师':
            if 'uname' in data:
                user.uname = data['uname']
            if 'pwd' in data:
                user.setPassword(data['pwd'])
            db.session.commit()
            return response
        else:
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

    @jwt_required()
    def delete(self, uid: int = None):
        response = response_base.copy()
        cur_uid = get_jwt_identity()

        role = User.getRoleByUid(cur_uid)

        if role == '管理员':
            if uid is None:
                data = request.get_json()
                uids = data['uids']
                db.session.query(User).filter(User.uid.in_(uids)).delete(synchronize_session=False)
                db.session.commit()
                return response
            user = db.session.query(User).filter(User.uid == uid).first()
            db.session.delete(user)
            db.session.commit()
            return response
        elif role == '教师':
            if uid is None:
                data = request.get_json()
                uids = data['uids']
                # 删除uid在uids中 且 role为学生的用户
                db.session.query(User).filter(User.uid.in_(uids), User.role == '学生').delete(synchronize_session=False)
                db.session.commit()
                return response
            user = db.session.query(User).filter(User.uid == uid).first()
            if user.role == '学生':
                db.session.delete(user)
                db.session.commit()
                return response
            else:
                response['code'] = 403
                response['msg'] = 'permission denied'
                return response
        else:
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response
