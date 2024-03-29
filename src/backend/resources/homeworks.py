from datetime import datetime

from .ext import *
from sqlalchemy import func, and_
from random import choices


class Homeworks(restful.Resource):
    @jwt_required()
    def get(self):
        response = response_base.copy()

        cur_uid = get_jwt_identity()

        if check_permission(cur_uid, ['管理员', '教师']):
            response['code'] = 400
            response['msg'] = '？？你在干什么'
            return response

        # 去Homework表中查找是否有当前用户的作业
        # 查找RUQ表中是否有没Used的记录
        ruq_query = db.session.query(RUQ).filter(and_(RUQ.uid == cur_uid, RUQ.used == False))
        ruq = ruq_query.all()
        if len(ruq) == 0:
            homeworks = db.session.query(Homework).filter_by(uid=cur_uid).order_by(Homework.timestamp.desc()).first()
            if homeworks:
                qids = homeworks.qids
                qids = qids.split(',')
                qids = [int(qid) for qid in qids]
                questions = db.session.query(Question).filter(Question.qid.in_(qids)).all()
                questions = {str(q.qid): q.qname for q in questions}
                data = []
                for qid in qids:
                    data.append(questions[str(qid)])
                response['data'] = data
                response['qids'] = qids
                return response
            else:
                response['code'] = 404
                response['msg'] = '没有错题！很优秀！'
                return response
        else:
            ruq_query.update({'used': True})

        wrong_qids = set()

        for r in ruq:
            r.used = True
            wrong_qids.add(r.qid)

        # 去RUQ表中查找当前用户的所有题目错误的知识点，并对pid分组计数
        rpq_sub = db.session.query(RPQ).subquery()
        wrong_pid = db.session.query(
            rpq_sub.c.pid.label('pid'),
            func.count(rpq_sub.c.pid).label('count'),
        ).filter(
            rpq_sub.c.qid.in_(wrong_qids),
        ).group_by(rpq_sub.c.pid).all()

        pid_dict = {str(w.pid): w.count for w in wrong_pid}

        question_set = set()
        # 根据pid去RPQ表中查找对应数量的qid
        for pid in wrong_pid:
            rpq = db.session.query(RPQ).filter_by(pid=pid.pid).all()
            qids = choices(rpq, k=pid.count)
            for r in qids:
                question_set.add(r.qid)

        question_less_set = set()
        for qid in question_set:
            # 查询pid，在pid_dict中的计数-1

            pid = db.session.query(RPQ).filter_by(qid=qid).all()
            pid = {str(p.pid) for p in pid}
            jiao = pid & set(pid_dict.keys())
            if len(jiao) == 0:
                continue
            question_less_set.add(qid)
            for p in pid:
                if p not in pid_dict:
                    continue
                pid_dict[p] -= 1
                if pid_dict[p] <= 0:
                    del pid_dict[p]
                if len(pid_dict) == 0:
                    break

        question_less_set -= wrong_qids
        # 根据qid去Question表中查找对应的题目
        questions = db.session.query(Question).filter(Question.qid.in_(question_less_set)).all()

        qs = [{
            'qid': q.qid,
            'qname': q.qname,
            'level': q.level,
        } for q in questions]

        hm = Homework()
        hm.uid = cur_uid
        hm.qids = ','.join([str(q['qid']) for q in qs])
        hm.timestamp = datetime.now()

        db.session.add(hm)
        db.session.commit()

        response['data'] = [q['qname'] for q in qs]
        return response

    @jwt_required()
    def post(self):
        response = response_base.copy()

        cur_uid = get_jwt_identity()

        if check_permission(cur_uid, ['管理员', '教师']):
            response['code'] = 400
            response['msg'] = '？？你在干什么'
            return response

        data = request.get_json()
        if 'qids' not in data:
            response['code'] = 400
            response['msg'] = '参数错误'
            return response
        qids = data['qids']

        db.session.execute(
            RUQ.__table__.insert(),
            [{"uid": cur_uid, "qid": qid, 'used': False} for qid in qids]
        )
        db.session.commit()

        return response
