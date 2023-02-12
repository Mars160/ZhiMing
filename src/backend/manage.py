# 按照models.py中的定义创建数据库表
from models import *
from ext import engine
Base.metadata.create_all(engine)
