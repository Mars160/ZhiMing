from .ext import *


class Role(restful.Resource):
    @jwt_required()
    def get(self):
        response = response_base.copy()

        cur_uid = get_jwt_identity()

        user = db.session.query(User).filter(User.uid == cur_uid).first()
        response['data'] = user.role
        return response
