from .ext import *


class Teachers(restful.Resource):
    @jwt_required(refresh=True)
    def get(self):
        response = response_base.copy()

        uid = get_jwt_identity()
        user = session.query(User).filter(User.uid == uid).first()
        if user is None:
            response['code'] = -1
            response['msg'] = 'user not found'
            return response
        else:
            if not check_permission(uid, ['管理员']):
                response['msg'] = 'permission denied'
                response['code'] = 403
                return response
            else:
                # 获取url中的参数
                limit = request.args.get('limit', 10, type=int)
                page = request.args.get('page', 1, type=int)
                teachers = session.query(User).filter(User.role == '教师').limit(limit).offset((page - 1) * limit).all()
                response['data'] = {}
                for teacher in teachers:
                    response['data'][teacher.uid] = teacher.uname
            return response

    @jwt_required(refresh=True)
    def post(self):
        response = response_base.copy()
        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        data = request.get_json()
        if 'tid' in data:
            uid = data['tid']
        else:
            uid = None
        uname = data['tname']

        user = session.query(User).filter(User.uid == uid).first()
        if user is None:
            user = User()
            user.uid = uid
            user.uname = uname
            user.role = '教师'
            user.setPassword(None)
            session.add(user)
            session.commit()
            response['data'] = str(user.uid)
            return response
        else:
            response['code'] = 400
            response['msg'] = 'user already exists'
            return response

    @jwt_required(refresh=True)
    def put(self, tid: int):
        response = response_base.copy()
        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        data = request.get_json()
        uname = data['tname']

        user = session.query(User).filter(User.uid == tid).first()
        if user is None:
            response['code'] = 404
            response['msg'] = 'user not found'
            return response
        else:
            user.uname = uname
            if 'pwd' in data:
                user.setPassword(data['pwd'])
            session.add(user)
            session.commit()
            return response

    @jwt_required(refresh=True)
    def delete(self, tid: int):
        response = response_base.copy()
        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        user = session.query(User).filter(User.uid == tid).first()
        if user is None:
            response['code'] = 404
            response['msg'] = 'user not found'
            return response
        else:
            session.delete(user)
            session.commit()
            return response
