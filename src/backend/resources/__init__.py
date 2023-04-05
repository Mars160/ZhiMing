from .ext import restful

from .token import Token
from .password import Password
from .teachers import Teachers
from .books import Books
from .questions import Questions
from .points import Points
from .role import Role
from .users import Users
from .classes import Classes
from .homeworks import Homeworks

api = restful.Api()

api.add_resource(Token, '/v1/token')
api.add_resource(Password, '/v1/password')
api.add_resource(Teachers, '/v1/teachers/<int:tid>', '/v1/teachers')
api.add_resource(Books, '/v1/books/<int:bid>', '/v1/books')
api.add_resource(Questions, '/v1/questions/<int:qid>', '/v1/questions')
api.add_resource(Points, '/v1/points/<int:pid>', '/v1/points')
api.add_resource(Role, '/v1/role')
api.add_resource(Users, '/v1/users/<int:uid>', '/v1/users')
api.add_resource(Classes, '/v1/classes/<int:cid>', '/v1/classes')
api.add_resource(Homeworks, '/v1/homeworks')
