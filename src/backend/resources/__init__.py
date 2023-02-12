from .ext import restful

from .token import Token
from .password import Password
from .teachers import Teachers
from .books import Books

api = restful.Api()

api.add_resource(Token, '/v1/token')
api.add_resource(Password, '/v1/password')
api.add_resource(Teachers, '/v1/teachers/<int:tid>', '/v1/teachers')
api.add_resource(Books, '/v1/books/<int:bid>', '/v1/books')
