from sqlalchemy import func

from .ext import *


class Books(restful.Resource):
    @jwt_required()
    def get(self):
        response = response_base.copy()
        # uid = get_jwt_identity()

        limit = request.args.get('limit', 10, type=int)
        page = request.args.get('page', 1, type=int)
        books = db.session.query(Book).limit(limit).offset((page - 1) * limit)

        book_a = books.all()
        response['data'] = {}
        response['data'] = [{"bid": i.bid, "bname": i.bname, "grade": i.grade, 'qcount': 0} for i in book_a]

        books = books.subquery()
        re = db.session.query(
            books.c.bid,
            func.count(RQB.qid).label('count'),
        ).filter(books.c.bid == RQB.bid).group_by(RQB.bid).all()
        # 根据bid更新response中的qcount
        bid2count = {}
        for i in re:
            bid2count[str(i.bid)] = i.count
        for i in response['data']:
            i['qcount'] = bid2count[str(i['bid'])] if str(i['bid']) in bid2count else 0

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

        # 删除RQB表中，bid为bid的记录
        rqbs.delete(synchronize_session=False)
        db.session.query(RPQ).filter(RPQ.qid.in_(q_list)).delete(synchronize_session=False)
        db.session.query(RUQ).filter(RUQ.qid.in_(q_list)).delete(synchronize_session=False)
        # 删除Question表中，qid在q_list中的记录
        db.session.query(Question).filter(Question.qid.in_(q_list)).delete(synchronize_session=False)
        # 删除Book表中，bid为bid的记录
        db.session.query(Book).filter(Book.bid == bid).delete(synchronize_session=False)

        db.session.commit()
        return response
