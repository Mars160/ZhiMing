import math

TEACHET_COUNT = 5
STUDENT_EACH_TEACHER = 30
BOOK_COUNT = 5
QUESTION_EACH_BOOK = 100
POINTS_COUNT = 30
POINTS_MAX_EACH_QUESTION = 5
MAX_PAGE = 30

from app import app
import click
from faker import Faker
from random import randint, choices
from models import *

fake = Faker(locale='zh_CN')


def create_db():
    db.create_all()


def create_admin(name, pwd):
    admin = User()
    admin.uid = 0
    admin.uname = name
    admin.role = '管理员'
    admin.nickname = fake.name()
    admin.setPassword(pwd)
    db.session.add(admin)
    db.session.commit()


def create_teachers(name, pwd):
    teacher = User()
    teacher.uname = name
    teacher.role = '教师'
    teacher.nickname = fake.name()
    teacher.setPassword(pwd)
    db.session.add(teacher)
    for i in range(TEACHET_COUNT - 1):
        teacher = User()
        teacher.uname = fake.user_name() + str(i)
        teacher.role = '教师'
        teacher.nickname = fake.name()
        teacher.setPassword(pwd)
        db.session.add(teacher)
    db.session.commit()


def create_student(name, pwd):
    teacher_count = db.session.query(User).filter(User.role == '教师').count()
    student = User()
    student.uname = name
    student.role = '学生'
    student.nickname = fake.name()
    student.setPassword(pwd)
    db.session.add(student)
    for i in range(STUDENT_EACH_TEACHER * teacher_count - 1):
        student = User()
        student.uname = fake.user_name() + str(i)
        student.role = '学生'
        student.nickname = fake.name()
        student.setPassword(pwd)
        db.session.add(student)
    db.session.commit()


def create_book():
    for i in range(BOOK_COUNT):
        book = Book()
        book.bname = fake.sentence(nb_words=2, variable_nb_words=True)
        book.grade = 41
        db.session.add(book)
    db.session.commit()


def create_points():
    for i in range(POINTS_COUNT):
        point = Point()
        point.pname = fake.sentence(nb_words=2, variable_nb_words=False)
        db.session.add(point)
    db.session.commit()


def create_question():
    books = db.session.query(Book.bid).all()
    pids = db.session.query(Point.pid).all()
    MAX_PLACE = math.ceil(QUESTION_EACH_BOOK / MAX_PAGE)
    for book in books:
        for i in range(QUESTION_EACH_BOOK):
            question = Question()
            question.qname = fake.sentence(nb_words=2, variable_nb_words=True)
            question.level = 1
            db.session.add(question)
            db.session.flush()

            rqb = RQB()
            rqb.bid = book.bid
            rqb.qid = question.qid
            rqb.page = randint(1, MAX_PAGE)
            rqb.place = randint(1, MAX_PLACE)
            db.session.add(rqb)

            # 随机选择不超过POINTS_MAX_EACH_QUESTION个知识点
            points = choices(pids, k=randint(1, POINTS_MAX_EACH_QUESTION))
            for point in points:
                rqp = RPQ()
                rqp.qid = question.qid
                rqp.pid = point.pid
                db.session.add(rqp)

    db.session.commit()


@app.cli.command('create')
@click.argument('item', default='None')
def create(item):
    if item == 'db':
        create_db()
        click.echo('数据库创建成功')
    elif item == 'admin':
        name = click.prompt('请输入管理员用户名', default='admin')
        pwd = click.prompt('请输入管理员密码', default='admin')
        create_admin(name, pwd)
        click.echo('管理员账号创建成功')
    elif item == 'teacher':
        name = click.prompt('请输入教师用户名', default='teacher')
        pwd = click.prompt('请输入教师密码', default='123456')
        create_teachers(name, pwd)
        click.echo('教师账号创建成功')
    elif item == 'student':
        name = click.prompt('请输入学生用户名', default='student')
        pwd = click.prompt('请输入学生密码', default='123456')
        create_student(name, pwd)
        click.echo('学生账号创建成功')
    elif item == 'book':
        create_book()
        click.echo('教材创建成功')
    elif item == 'points':
        create_points()
        click.echo('知识点创建成功')
    elif item == 'question':
        create_question()
        click.echo('题目创建成功')

    elif item == 'prod':
        create_db()
        create_admin('admin', 'admin')
        click.echo('生产环境数据创建成功')
    elif item == 'all' or item == 'test':
        create_db()
        click.echo('数据库创建成功...')
        create_admin('admin', 'admin')
        click.echo('管理员账号创建成功...')
        create_teachers('teacher', 'teacher')
        click.echo('教师账号创建成功...')
        create_student('student', 'student')
        click.echo('学生账号创建成功...')
        create_book()
        click.echo('教材创建成功...')
        create_points()
        click.echo('知识点创建成功...')
        create_question()
        click.echo('题目创建成功...')
        click.echo('所有数据创建成功')
    else:
        click.echo('参数错误，可选参数：db, admin, teacher, student, book, points, question, prod, all, test')


@app.cli.command('drop-db')
def drop_db():
    db.drop_all()
    click.echo('数据库删除成功')

