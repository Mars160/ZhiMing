from .ext import *


class Questions(restful.Resource):
    @jwt_required()
    def get(self):
        response = response_base.copy()

        uid = get_jwt_identity()
        user = session.query(User).filter(User.uid == uid).first()
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

            # questions = session.query(Question).order_by(
            #     getattr(
            #         getattr(Question, orderby),                        order)()
            # ).limit(limit).offset((page - 1) * limit).all()
            questions = session.query(Question).limit(limit).offset((page - 1) * limit).subquery()
            p_q = session.query(questions, RPQ).join(RPQ, RPQ.qid == questions.c.qid).subquery()
            p_q_name = session.query(p_q, Point).join(Point, Point.pid == p_q.c.pid).all()
            response['data'] = {}
            for question in p_q_name:
                qid = question[0].qid
                if qid not in response['data']:
                    response['data'][qid] = {
                        'qname': question[0].qname,
                        'level': question[0].level,
                        'points': []
                    }
                response['data'][qid]['points'].append(
                    {question[1].pid: question[2].pname}
                )
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

            session.add(question)

            # 在RQB表中添加记录
            rqb = RQB()
            rqb.bid = bid
            rqb.qid = question.qid
            rqb.page = page
            rqb.place = place
            session.add(rqb)

            # 在RPQ表中添加记录
            for i in point:
                rpq = RPQ()
                rpq.qid = question.qid
                rpq.pid = i
                session.add(rpq)

            session.commit()

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

            q = session.query(Question).filter(Question.qid == qid).first()
            if q is None:
                response['code'] = 404
                response['msg'] = 'question not found'
                return response
            o_bid = q.bid  # 原bid
            q.bid = bid
            q.qname = qname

            # 在RQB表中修改记录
            rqb = session.query(RQB).filter(RQB.qid == qid, RQB.bid == o_bid).first()
            rqb.bid = bid
            rqb.qid = qid
            rqb.page = page
            rqb.place = place

            # 在RPQ表中修改记录
            session.query(RPQ).filter(RPQ.qid == qid).delete()
            for i in point:
                rpq = RPQ()
                rpq.qid = qid
                rpq.pid = i
                session.add(rpq)

            session.commit()
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
        session.query(RPQ).filter(RPQ.qid == qid).delete()
        # 删除RQB表中的记录
        session.query(RQB).filter(RQB.qid == qid).delete()
        # 删除Question表中的记录
        session.query(Question).filter(Question.qid == qid).delete()
        session.commit()
        return response











