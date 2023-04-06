# Orm models
from json import dumps
from werkzeug.security import generate_password_hash, check_password_hash

from ext import db

Column = db.Column
Integer = db.Integer
VARCHAR = db.VARCHAR
TEXT = db.TEXT
ForeignKey = db.ForeignKey
TIMESTAMP = db.TIMESTAMP
Boolean = db.Boolean


class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = (
        {'comment': '用户表'}
    )
    uid = Column(Integer, primary_key=True, autoincrement=True, comment='用户id')
    uname = Column(VARCHAR(20), nullable=False, comment='用户名', unique=True)
    role = Column(VARCHAR(10), nullable=False, comment='用户角色')
    nickname = Column(VARCHAR(20), nullable=False, comment='用户昵称')
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
            if len(str_id) <= 6:
                str_id = '0' * (6 - len(str_id)) + str_id
            pwd = 'ZhiMing' + str_id
        #self.pwd = pwd
        self.pwd = generate_password_hash(pwd)

    def checkPassword(self, pwd):
        if check_password_hash(self.pwd, pwd) or self.pwd == pwd:
            return True


class Book(db.Model):
    __tablename__ = 'Book'
    __table_args__ = (
        {'comment': '练习册表'}
    )
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
    __table_args__ = (
        {'comment': '题目表'}
    )
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
    __table_args__ = (
        {'comment': '班级表'}
    )
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
    __table_args__ = (
        {'comment': '知识点表'}
    )
    pid = Column(Integer, primary_key=True, autoincrement=True, comment='知识点id')
    pname = Column(VARCHAR(500), nullable=False, comment='知识点名称')

    def __repr__(self):
        return dumps({
            'pid': self.pid,
            'pname': self.pname
        })


class RUC(db.Model):
    __tablename__ = 'RUC'
    __table_args__ = (
        {'comment': '用户班级关系表'}
    )
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
    __table_args__ = (
        {'comment': '题目练习册关系表'}
    )
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
    __table_args__ = (
        {'comment': '知识点题目关系表'}
    )
    pqid = Column(Integer, primary_key=True, autoincrement=True, comment='关系id')
    pid = Column(Integer, ForeignKey('Point.pid'), nullable=False, comment='知识点id')
    qid = Column(Integer, ForeignKey('Question.qid'), nullable=False, comment='题目id')

    def __repr__(self):
        return dumps({
            'pqid': self.pqid,
            'pid': self.pid,
            'qid': self.qid
        })


class RUQ(db.Model):
    __tablename__ = 'RUQ'
    __table_args__ = ({
        'comment': '用户错了的题目'
    })
    uqid = Column(Integer, primary_key=True, autoincrement=True, comment='关系id')
    uid = Column(Integer, ForeignKey('User.uid'), nullable=False, comment='用户id')
    qid = Column(Integer, ForeignKey('Question.qid'), nullable=False, comment='题目id')
    used = Column(Boolean, nullable=False, comment='是否已经使用过')


    def __repr__(self):
        return dumps({
            'uqid': self.uqid,
            'uid': self.uid,
            'qid': self.qid
        })


class Homework(db.Model):
    __tablename__ = 'Homework'
    __table_args__ = ({
        'comment': '平台生成的作业表'
    })
    hid = Column(Integer, primary_key=True, autoincrement=True, comment='作业id')
    uid = Column(Integer, ForeignKey('User.uid'), nullable=False, comment='用户id')
    qids = Column(TEXT, nullable=False, comment='题目id列表')
    timestamp = Column(TIMESTAMP, nullable=False, comment='生成时间')

    def __repr__(self):
        return dumps({
            'hid': self.hid,
            'uid': self.uid,
            'qids': self.qids
        })



