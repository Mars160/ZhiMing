from plugins.tunnel import *
import flask_restful as restful


# 如果要添加新的endpoint，建议加一个plugin前缀用于标注为插件，例如/v1/plugin/ocr
# code below this line，以下代码都会执行

class Helloworld(restful.Resource):
    def get(self):
        return {
            "code": 0,
            "data": None,
            "msg": "Hello World"
        }


api = get_global('api')
resources = api.resources
flag = None
for r in resources:
    if r[1][0] == '/v1/ping':
        flag = r
api.resources.remove(flag)
api.add_resource(Helloworld, '/v1/ping')
