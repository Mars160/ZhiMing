from .ext import *


class Ping(restful.Resource):
    def get(self):
        response = response_base.copy()
        response['msg'] = 'pong'
        return response

