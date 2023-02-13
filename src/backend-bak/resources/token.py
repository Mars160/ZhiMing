from .ext import *
from flask_jwt_extended import create_refresh_token


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
                response['data'] = create_refresh_token(identity=name)
                return response
            else:
                response['code'] = 403
                response['msg'] = 'password error'
                return response
