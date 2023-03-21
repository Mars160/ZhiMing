from .ext import *


class Questions(restful.Resource):
    @jwt_required()
    def get(self):
        response = response_base.copy()

        uid = get_jwt_identity()
        user = db.session.query(User).filter(User.uid == uid).first()
        if not check_permission(user.uid, ['教师', '管理员']):
            response['msg'] = 'permission denied'
            response['code'] = 403
            return response
        else:
            # 获取url中的参数
            limit = request.args.get('limit', 10, type=int)
            page = request.args.get('page', 1, type=int)
            orderby = request.args.get('orderby', 'qid', type=str)
            order = request.args.get('order', 'asc', type=str)
            bid = request.args.get('bid', None, type=int)
            if bid is None:
                response['code'] = 400
                response['msg'] = 'parameter bid is required'
                return response

            b_q = db.session.query(RQB).filter(RQB.bid == bid).subquery()
            # 从RPQ中获取pid
            b_q_p = db.session.query(b_q, RPQ).join(RPQ, RPQ.qid == b_q.c.qid).subquery()

            b_qname_p = db.session.query(b_q_p, Question).join(Question, Question.qid == b_q_p.c.qid).subquery()
            b_qname_pname = db.session.query(b_qname_p, Point).join(Point, Point.pid == b_qname_p.c.pid).all()

            response['data'] = []
            # for question in b_qname_pname:
            #     qid = question[0].qid
            #     if qid not in response['data']:
            #         response['data'][qid] = {
            #             'qname': question[0].qname,
            #             'level': question[0].level,
            #             'points': []
            #         }
            #     response['data'][qid]['points'].append(
            #         {question[1].pid: question[2].pname}
            #     )
            question_dict = {}
            for row in b_qname_pname:
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

            question = Question()
            question.qname = qname
            question.level = ''

            db.session.add(question)

            # 在RQB表中添加记录
            rqb = RQB()
            rqb.bid = bid
            rqb.qid = question.qid
            rqb.page = page
            rqb.place = place
            db.session.add(rqb)

            # 在RPQ表中添加记录
            for i in point:
                rpq = RPQ()
                rpq.qid = question.qid
                rpq.pid = i
                db.session.add(rpq)

            db.session.commit()

            response['data'] = question.qid
            return response

    @jwt_required()
    def put(self, qid:int):
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

            q = db.session.query(Question).filter(Question.qid == qid).first()
            if q is None:
                response['code'] = 404
                response['msg'] = 'question not found'
                return response
            o_bid = q.bid  # 原bid
            q.bid = bid
            q.qname = qname

            # 在RQB表中修改记录
            rqb = db.session.query(RQB).filter(RQB.qid == qid, RQB.bid == o_bid).first()
            rqb.bid = bid
            rqb.qid = qid
            rqb.page = page
            rqb.place = place

            # 在RPQ表中修改记录
            db.session.query(RPQ).filter(RPQ.qid == qid).delete()
            for i in point:
                rpq = RPQ()
                rpq.qid = qid
                rpq.pid = i
                db.session.add(rpq)

            db.session.commit()
            return response

    @jwt_required()
    def delete(self, qid:int):
        response = response_base.copy()

        cur_uid = get_jwt_identity()
        if not check_permission(cur_uid, ['教师', '管理员']):
            response['code'] = 403
            response['msg'] = 'permission denied'
            return response

        # 删除RPQ表中的记录
        db.session.query(RPQ).filter(RPQ.qid == qid).delete()
        # 删除RQB表中的记录
        db.session.query(RQB).filter(RQB.qid == qid).delete()
        # 删除Question表中的记录
        db.session.query(Question).filter(Question.qid == qid).delete()
        db.session.commit()
        return response











