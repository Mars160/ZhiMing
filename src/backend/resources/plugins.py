from .ext import *
import os
from ext import STATIC_FOLDER

class Plugins(restful.Resource):
    def get(self):
        response = response_base.copy()
        type_ = request.args.get('type', default='name')

        if type_ == 'name':
            plugins = os.listdir(STATIC_FOLDER)
            if '__pycache__' in plugins:
                plugins.remove('__pycache__')
            response['data'] = plugins
        elif type_ == 'components':
            # 扫描STATIC_FOLDER及其子目录下的所有vue文件
            # 生成一个字典，key为文件名，value为文件路径
            # 例如：{'index.vue': STATIC_FOLDER + '/zhiming-paddle-ocr-plugin/index.vue'}
            components = {}
            for root, dirs, files in os.walk(STATIC_FOLDER):
                for file in files:
                    if file.endswith('.vue'):
                        comp_name = file.split('.')[0]
                        components[comp_name] = os.path.join(root, file).replace('\\', '/').replace(STATIC_FOLDER, 'plugin')
            response['data'] = components
        return response


