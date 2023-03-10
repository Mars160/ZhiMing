# Orm models
from json import dumps
from werkzeug.security import generate_password_hash, check_password_hash

from ext import db

Column = db.Column
Integer = db.Integer
VARCHAR = db.VARCHAR
TEXT = db.TEXT
ForeignKey = db.ForeignKey


class User(db.Model):
    __tablename__ = 'User'
    uid = Column(Integer, primary_key=True, autoincrement=True, comment='用户id')
    uname = Column(VARCHAR(20), nullable=False, comment='用户名')
    role = Column(VARCHAR(10), nullable=False, comment='用户角色')
    pwd = Column(TEXT, nullable=False, comment='用户密码')

    __cache = {}

    @staticmethod
    def getRoleByUid(uid):
        if uid not in User.__cache:
            user = db.session.query(User).filter(User.uid == uid).first()
            User.__cache[uid] = user.role
        return User.__cache[uid]



    def __repr__(self):
        # 以json格式返回
        return dumps({
            'uid': self.uid,
            'uname': self.uname,
            'role': self.role,
            'pwd': self.pwd
        })

    def setPassword(self, pwd):
        if pwd is None:
            str_id = str(self.uid)
            if len(str_id) < 6:
                str_id = '0' * (6 - len(str_id)) + str_id
            pwd = 'ZhiMing' + str_id
        self.pwd = generate_password_hash(pwd)

    def checkPassword(self, pwd):
        return check_password_hash(self.pwd, pwd)


class Book(db.Model):
    __tablename__ = 'Book'
    bid = Column(Integer, primary_key=True, autoincrement=True, comment='练习册id')
    bname = Column(VARCHAR(500), nullable=False, comment='练习册名称', unique=True)
    grade = Column(Integer, nullable=False, comment='适用年级')

    def __repr__(self):
        return dumps({
            'bid': self.bid,
            'bname': self.bname,
            'grade': self.grade
        })


class Question(db.Model):
    __tablename__ = 'Question'
    qid = Column(Integer, primary_key=True, autoincrement=True, comment='题目id')
    qname = Column(TEXT, nullable=False, comment='题干')
    level = Column(Integer, nullable=False, comment='难度等级')

    def __repr__(self):
        return dumps({
            'qid': self.qid,
            'qname': self.qname,
            'level': self.level
        })


class Class(db.Model):
    __tablename__ = 'Class'
    cid = Column(Integer, primary_key=True, autoincrement=True, comment='班级id')
    cname = Column(VARCHAR(50), nullable=False, comment='班级名称', unique=True)
    grade = Column(Integer, nullable=False, comment='年级')

    def __repr__(self):
        return dumps({
            'cid': self.cid,
            'cname': self.cname,
            'grade': self.grade
        })


class Point(db.Model):
    __tablename__ = 'Point'
    pid = Column(Integer, primary_key=True, autoincrement=True, comment='知识点id')
    pname = Column(VARCHAR(500), nullable=False, comment='知识点名称')

    def __repr__(self):
        return dumps({
            'pid': self.pid,
            'pname': self.pname
        })


class RUC(db.Model):
    __tablename__ = 'RUC'
    ucid = Column(Integer, primary_key=True, autoincrement=True, comment='关系id')
    uid = Column(Integer, ForeignKey('User.uid'), nullable=False, comment='用户id')
    cid = Column(Integer, ForeignKey('Class.cid'), nullable=False, comment='班级id')

    def __repr__(self):
        return dumps({
            'ucid': self.ucid,
            'uid': self.uid,
            'cid': self.cid
        })


class RQB(db.Model):
    __tablename__ = 'RQB'
    qbid = Column(Integer, primary_key=True, autoincrement=True, comment='关系id')
    qid = Column(Integer, ForeignKey('Question.qid'), nullable=False, comment='题目id')
    bid = Column(Integer, ForeignKey('Book.bid'), nullable=False, comment='练习册id')
    page = Column(Integer, nullable=False, comment='页码')
    place = Column(Integer, nullable=False, comment='位置')

    def __repr__(self):
        return dumps({
            'qbid': self.qbid,
            'qid': self.qid,
            'bid': self.bid,
            'page': self.page,
            'place': self.place
        })


class RPQ(db.Model):
    __tablename__ = 'RPQ'
    pqid = Column(Integer, primary_key=True, autoincrement=True, comment='关系id')
    pid = Column(Integer, ForeignKey('Point.pid'), nullable=False, comment='知识点id')
    qid = Column(Integer, ForeignKey('Question.qid'), nullable=False, comment='题目id')

    def __repr__(self):
        return dumps({
            'pqid': self.pqid,
            'pid': self.pid,
            'qid': self.qid
        })
