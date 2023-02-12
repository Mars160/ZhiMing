from .ext import *


class Token(restful.Resource):
    def get(self):
        response = response_base.copy()

        data = request.get_json()
        name = data['user']
        pwd = data['pwd']

        user = session.query(User).filter(User.uid == name).first()
        if user is None:
            response['code'] = 404
            response['msg'] = 'user not found'
            return response
        else:
            if user.checkPassword(pwd):
                response['data'] = create_access_token(identity=name, expires_delta=False)
                return response
            else:
                response['code'] = 403
                response['msg'] = 'password error'
                return response
