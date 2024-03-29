from .ext import *


class Students(restful.Resource):
    @jwt_required()
    def get(self):
        response = response_base.copy()
        uid = get_jwt_identity()

        if not check_permission(uid, ['管理员', '教师']):
            response['msg'] = 'permission denied'
            response['code'] = 403
            return response

        # 获取url中的参数
        limit = request.args.get('limit', 10, type=int)
        page = request.args.get('page', 1, type=int)
        students = db.session.query(User).filter(User.role == '学生').limit(limit).offset((page - 1) * limit).all()
        response['data'] = {}
        for stu in students:
            response['data'][stu.uid] = stu.uname
        return response

    @jwt_required()
    def post(self):
        response = response_base.copy()
        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['管理员', '教师']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        data = request.get_json()
        if 'sid' in data:
            uid = data['sid']
        else:
            uid = None
        uname = data['sname']

        user = db.session.query(User).filter(User.uid == uid).first()
        if user is None:
            user = User()
            user.uid = uid
            user.uname = uname
            user.role = '学生'
            user.setPassword(None)
            db.session.add(user)
            db.session.commit()
            response['data'] = user.uid
            return response
        else:
            response['code'] = 400
            response['msg'] = 'user already exists'
            return response

    @jwt_required()
    def put(self, tid: int):
        response = response_base.copy()
        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['管理员', '教师']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        data = request.get_json()
        uname = data['sname']

        user = db.session.query(User).filter(User.uid == tid).first()
        if user is None:
            response['code'] = 404
            response['msg'] = 'user not found'
            return response
        else:
            user.uname = uname
            if 'pwd' in data:
                user.setPassword(data['pwd'])
            db.session.add(user)
            db.session.commit()
            return response

    @jwt_required()
    def delete(self, tid: int):
        response = response_base.copy()
        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['管理员', '教师']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        user = db.session.query(User).filter(User.uid == tid).first()
        if user is None:
            response['code'] = 404
            response['msg'] = 'user not found'
            return response
        else:
            db.session.delete(user)
            db.session.commit()
            return response
