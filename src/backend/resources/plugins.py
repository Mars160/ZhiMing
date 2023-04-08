from .ext import *
import os
from ext import STATIC_FOLDER


class Plugins(restful.Resource):
    def get(self):
        response = response_base.copy()

        plugins = os.listdir(STATIC_FOLDER)
        if '__pycache__' in plugins:
            plugins.remove('__pycache__')
        response['data'] = plugins
