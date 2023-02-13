from .ext import *


class Points(restful.Resource):
    @jwt_required()
    def get(self):
        response = response_base.copy()

        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        limit = request.args.get('limit', 10, type=int)
        page = request.args.get('page', 1, type=int)

        points = session.query(Point).limit(limit).offset((page - 1) * limit).all()
        response['data'] = {}
        for point in points:
            response['data'][point.pid] = point.pname
        return response

    @jwt_required()
    def post(self):
        response = response_base.copy()

        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        data = request.get_json()
        pname = data['pname']

        point = Point(pname=pname)
        session.add(point)
        session.commit()
        response['data'] = point.pid
        return response

    @jwt_required()
    def put(self, pid:int):
        response = response_base.copy()

        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        data = request.get_json()
        pname = data['pname']

        point = session.query(Point).filter(Point.pid == pid).first()
        if point is None:
            response['code'] = 404
            response['msg'] = 'point not found'
            return response
        else:
            point.pname = pname
            session.commit()
            return response

    @jwt_required()
    def delete(self, pid:int):
        response = response_base.copy()

        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        point = session.query(Point).filter(Point.pid == pid).first()
        if point is None:
            response['code'] = 404
            response['msg'] = 'point not found'
            return response

        # 在RPQ表中删除该知识点
        session.query(RPQ).filter(RPQ.pid == pid).delete()
        session.delete(point)
        session.commit()
        return response



