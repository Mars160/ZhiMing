from .ext import *


class Classes(restful.Resource):
    @jwt_required()
    def get(self):
        response = response_base.copy()

        cur_uid = get_jwt_identity()

        if check_permission(cur_uid, ['管理员', '教师']):
            class_sub = db.session.query(Class).subquery()
            user_sub = db.session.query(User).subquery()
            ruc_sub = db.session.query(RUC).subquery()
            result = db.session.query(
                class_sub.c.cid.label('cid'),
                class_sub.c.cname.label('cname'),
                class_sub.c.grade.label('grade'),
                user_sub.c.uid.label('uid'),
                user_sub.c.uname.label('uname'),
                ruc_sub.c.role.label('role'),
            ).filter(
                class_sub.c.cid == ruc_sub.c.cid,
                user_sub.c.uid == ruc_sub.c.uid,
            ).all()
            classes = {}
            for r in result:
                cid = str(r.cid)
                if cid not in classes:
                    classes[cid] = {
                        'cid': r.cid,
                        'cname': r.cname,
                        'grade': r.grade,
                        'teachers': [],
                        'students': [],
                    }
                if r.role == '教师':
                    classes[cid]['teachers'].append({
                        'tid': r.uid,
                        'tname': r.uname,
                    })
                elif r.role == '学生':
                    classes[cid]['students'].append({
                        'sid': r.uid,
                        'sname': r.uname,
                    })

            response['data'] = [{
                'cid': cid,
                'cname': value['cname'],
                'grade': value['grade'],
                'teachers': value['teachers'],
                'students': value['students'],
            } for cid, value in classes.items()]
        else:
            response['code'] = 403
            response['msg'] = 'permission denied'

        return response

    @jwt_required()
    def post(self):
        response = response_base.copy()
        cur_uid = get_jwt_identity()
        data = request.get_json()
        if not data:
            response['code'] = 1
            response['msg'] = '参数错误'
            return response
        elif not data.get('cname'):
            response['code'] = 1
            response['msg'] = '班级名称不能为空'
            return response
        elif not data.get('grade'):
            response['code'] = 1
            response['msg'] = '年级不能为空'
            return response
        role = User.getRoleByUid(cur_uid)
        if role == '管理员' or role == '教师':
            c = Class()
            c.cname = data.get('cname')
            c.grade = data.get('grade')
            db.session.add(c)
            db.session.flush()

            if role == '管理员':
                tids = data.get('tids')
                for tid in tids:
                    ruc = RUC()
                    ruc.cid = c.cid
                    ruc.uid = tid
                    db.session.add(ruc)
            else:
                ruc = RUC()
                ruc.cid = c.cid
                ruc.uid = cur_uid
                db.session.add(ruc)

            sids = data.get('sids')
            for sid in sids:
                ruc = RUC()
                ruc.cid = c.cid
                ruc.uid = sid
                db.session.add(ruc)
        db.session.commit()
        return response

    @jwt_required()
    def put(self, cid: int):
        response = response_base.copy()

        cur_uid = get_jwt_identity()
        role = User.getRoleByUid(cur_uid)

        data = request.get_json()
        if not data:
            response['code'] = 1
            response['msg'] = '参数错误'
            return response

        if role == '管理员' or (role == '教师' and check_class_permission(cur_uid, cid)):
            c = db.session.query(Class).filter(Class.cid == cid).first()
            if not c:
                response['code'] = 404
                response['msg'] = '班级不存在'
                return response
            c.cname = data.get('cname')
            c.grade = data.get('grade')

            if 'sids' in data:
                sids = data.get('sids')
                db.session.query(RUC).filter(
                    (RUC.cid == cid) and (User.uid == RUC.uid) and (User.role == '学生')).delete()
                for sid in sids:
                    ruc = RUC()
                    ruc.cid = cid
                    ruc.uid = sid
                    db.session.add(ruc)
            if role == '管理员':
                if 'tids' in data:
                    tids = data.get('tids')
                    db.session.query(RUC).filter(
                        (RUC.cid == cid) and (User.uid == RUC.uid) and (User.role == '教师')).delete()
                    for tid in tids:
                        ruc = RUC()
                        ruc.cid = cid
                        ruc.uid = tid
                        db.session.add(ruc)
            db.session.commit()
        else:
            response['code'] = 403
            response['msg'] = 'permission denied'

        return response

    @jwt_required()
    def delete(self, cid: int):
        response = response_base.copy()

        cur_uid = get_jwt_identity()
        role = User.getRoleByUid(cur_uid)

        if role == '管理员' or (role == '教师' and check_class_permission(cur_uid, cid)):
            db.session.query(RUC).filter(RUC.cid == cid).delete()
            db.session.query(Class).filter(Class.cid == cid).delete()
            db.session.commit()
        else:
            response['code'] = 403
            response['msg'] = 'permission denied'

        return response

