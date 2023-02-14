# 按照models.py中的定义创建数据库表
from models import *
from ext import engine, session
Base.metadata.create_all(engine)

# 创建管理员账号

admin = User()
admin.uid = 0
admin.uname = 'admin'
admin.role = '管理员'
admin.setPassword('admin')
session.add(admin)
session.commit()
