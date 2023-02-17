from .ext import *


class Books(restful.Resource):
    @jwt_required()
    def get(self):
        response = response_base.copy()
        uid = get_jwt_identity()
        if not check_permission(uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        limit = request.args.get('limit', 10, type=int)
        page = request.args.get('page', 1, type=int)
        books = db.session.query(Book).limit(limit).offset((page - 1) * limit).all()
        response['data'] = {}
        response['data'] = [{"bid": i.bid, "bname": i.bname, "grade": i.grade} for i in books]
        return response

    @jwt_required()
    def post(self):
        response = response_base.copy()
        uid = get_jwt_identity()
        if not check_permission(uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        data = request.get_json()
        book = Book()
        book.bname = data['bname']
        book.grade = data['grade']
        db.session.add(book)
        db.session.commit()
        response['data'] = str(book.bid)
        return response

    @jwt_required()
    def put(self, bid):
        response = response_base.copy()
        uid = get_jwt_identity()
        if not check_permission(uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        data = request.get_json()
        book = db.session.query(Book).filter(Book.bid == bid).first()
        book.bname = data['bname']
        book.grade = data['grade']
        db.session.commit()
        return response

    @jwt_required()
    def delete(self, bid):
        response = response_base.copy()
        uid = get_jwt_identity()
        if not check_permission(uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        # 在RQB中查找是否有关联
        rqbs = db.session.query(RQB).filter(RQB.bid == bid)
        rqb_a = rqbs.all()
        q_list = [rqb.qid for rqb in rqb_a]

        # 删除Question表中，qid在q_list中的记录
        db.session.query(Question).filter(Question.qid.in_(q_list)).delete(synchronize_session=False)
        # 删除RQB表中，bid为bid的记录
        rqbs.delete(synchronize_session=False)
        # 删除Book表中，bid为bid的记录
        db.session.query(Book).filter(Book.bid == bid).delete(synchronize_session=False)

        db.session.commit()
        return response
