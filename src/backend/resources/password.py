from .ext import *


class Password(restful.Resource):
    @jwt_required()
    def put(self):
        response = response_base.copy()

        data = request.get_json()
        pwd = data['pwd']
        uid = get_jwt_identity()

        user = session.query(User).filter(User.uid == uid).first()
        if user is None:
            response['code'] = 1
            response['msg'] = 'user not found'
            return response
        else:
            user.setPassword(pwd)
            session.add(user)
            session.commit()
            return response
