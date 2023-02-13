from .ext import *


class Books(restful.Resource):
    @jwt_required(refresh=True)
    def get(self):
        response = response_base.copy()
        uid = get_jwt_identity()
        if not check_permission(uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        limit = request.args.get('limit', 10, type=int)
        page = request.args.get('page', 1, type=int)
        books = session.query(Book).limit(limit).offset((page - 1) * limit).all()
        response['data'] = {}
        for i in books:
            response['data'][i.id] = i.to_dict()
        return response

    @jwt_required(refresh=True)
    def post(self):
        response = response_base.copy()
        uid = get_jwt_identity()
        if not check_permission(uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        data = request.get_json()
        book = Book()
        book.name = data['bname']
        book.grade = data['grade']
        session.add(book)
        session.commit()
        response['data'] = str(book.bid)
        return response

    @jwt_required(refresh=True)
    def put(self, bid):
        response = response_base.copy()
        uid = get_jwt_identity()
        if not check_permission(uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        data = request.get_json()
        book = session.query(Book).filter(Book.bid == bid).first()
        book.name = data['bname']
        book.grade = data['grade']
        session.commit()
        return response

    @jwt_required(refresh=True)
    def delete(self, bid):
        response = response_base.copy()
        uid = get_jwt_identity()
        if not check_permission(uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        book = session.query(Book).filter(Book.bid == bid).first()
        session.delete(book)
        session.commit()
        return response
