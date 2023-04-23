from .ext import *
import numpy as np

class Questions(restful.Resource):
    UPDATE_TIME = 100
    COUNT_FROM = 3600

    @jwt_required()
    def get(self):
        response = response_base.copy()

        uid = get_jwt_identity()
        user = db.session.query(User).filter(User.uid == uid).first()

        # 获取url中的参数
        limit = request.args.get('limit', 10, type=int)
        page = request.args.get('page', 1, type=int)
        orderby = request.args.get('orderby', 'qid', type=str)
        order = request.args.get('order', 'asc', type=str)
        bid = request.args.get('bid', None, type=int)
        pagerange = request.args.get('pagerange', None, type=str)

        page_list = pagerange.split('-') if pagerange else None
        if bid is None:
            response['code'] = 400
            response['msg'] = 'parameter bid is required'
            return response

        ques = db.session.query(Question).filter(
            Question.bid == bid,
            Question.page >= (page_list[0] if page_list else 0),
            Question.page <= (page_list[1] if page_list else 999999)
        )

        # pages = ques.count() // limit + 1
        ques = ques.limit(limit).offset((page - 1) * limit).subquery()

        query = db.session.query(
            ques.c.bid,
            ques.c.page,
            ques.c.place,
            ques.c.qid,
            ques.c.qname,
            ques.c.level,
            RPQ.pid,
            Point.pname,
            RPQ.pqid,
        ).filter(
            RPQ.qid == ques.c.qid,
            RPQ.pid == Point.pid,
        ).all()

        response['data'] = []
        # response['pages'] = pages

        question_dict = {}
        for row in query:
            qid = row.qid
            if qid not in question_dict:
                question_dict[qid] = {
                    'qname': row.qname,
                    'level': row.level,
                    'points': [row.pname],
                    'page': row.page,
                    'place': row.place
                }
            else:
                question_dict[qid]['points'].append(row.pname)
        for qid in question_dict:
            item = {
                'qid': qid,
                'qname': question_dict[qid]['qname'],
                'level': question_dict[qid]['level'],
                'points': question_dict[qid]['points'],
                'page': question_dict[qid]['page'],
                'place': question_dict[qid]['place']
            }
            response['data'].append(item)
        return response

    @jwt_required()
    def post(self):
        response = response_base.copy()

        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response
        else:
            data = request.get_json()

            bid = data['bid']
            qname = data['qname']
            point = data['point']
            page = data['page']
            place = data['place']
            level = data['level'] if 'level' in data else 0

            # 查看bid是否存在
            book = db.session.query(Book).filter(Book.bid == bid).first()
            if book is None:
                response['code'] = 404
                response['msg'] = 'book not found'
                return response

            question = Question()
            question.qname = qname
            question.level = level
            question.bid = bid
            question.place = place
            question.page = page

            db.session.add(question)
            db.session.flush()

            with db.session.no_autoflush:
                self.add_not_exist_point(point, question.qid)

            db.session.commit()

            response['data'] = question.qid
            return response

    @jwt_required()
    def put(self, qid: int):
        response = response_base.copy()

        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response
        else:
            data = request.get_json()

            qname = data['qname']
            point = data['point']
            page = data['page']
            place = data['place']

            q = db.session.query(Question).filter(Question.qid == qid).first()
            if q is None:
                response['code'] = 404
                response['msg'] = 'question not found'
                return response
            q.qname = qname
            q.page = page
            q.place = place

            # 在RPQ表中修改记录
            db.session.query(RPQ).filter(RPQ.qid == qid).delete()

            with db.session.no_autoflush:
                self.add_not_exist_point(point, qid)

            db.session.commit()
            return response

    @jwt_required()
    def delete(self, qid: int):
        response = response_base.copy()

        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        # 删除RPQ表中的记录
        db.session.query(RPQ).filter(RPQ.qid == qid).delete()

        db.session.query(RUQ).filter(RUQ.qid == qid).delete()
        # 删除Question表中的记录
        db.session.query(Question).filter(Question.qid == qid).delete()
        db.session.commit()
        return response

    def add_not_exist_point(self, point, qid):
        # point为pname列表，使用in从数据库筛选出pid列表，若不存在则添加到point表中
        exist_ps = db.session.query(Point.pid, Point.pname).filter(Point.pname.in_(point)).all()
        exist_pids = []
        exist_pnames = []
        for i in exist_ps:
            exist_pids.append(i[0])
            exist_pnames.append(i[1])

        # 不存在的pname
        new_pnames = list(set(point) - set(exist_pnames))
        if len(new_pnames) > 0:
            db.session.execute(
                Point.__table__.insert(),
                [{'pname': i} for i in new_pnames]
            )
            # 获取新添加的pid
            new_pids = db.session.query(Point.pid).filter(Point.pname.in_(new_pnames)).all()
            for i in new_pids:
                exist_pids.append(i[0])
            db.session.execute(
                RPQ.__table__.insert(),
                [{'qid': qid, 'pid': i} for i in exist_pids]
            )

        self.UPDATE_TIME -= 1

        if self.UPDATE_TIME == 0:
            self.UPDATE_TIME = 100
            exist_pids = db.session.query(RPQ.pid).all()
            # 清除不在RPQ表中的point
            db.session.query(Point).filter(~Point.pid.in_(exist_pids)).delete()
