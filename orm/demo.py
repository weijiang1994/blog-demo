from email.policy import default
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1994124@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TimestampMixin(object):

    @declared_attr
    def created_time(cls):
        return db.Column(db.DateTime, default=datetime.now)

    @declared_attr
    def updated_time(cls):
        return db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Employee(TimestampMixin, db.Model):
    __tablename__ = 'emp'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), default='')
    password = db.Column(db.String(128), default='')
    department = db.Column(db.INTEGER, default=0, comment='')

    def __init__(self, username, password, department):
        self.username = username
        self.password = password
        self.department = department


class Department(TimestampMixin, db.Model):
    __tablename__ = 'dept'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), default='')

    def __init__(self, name):
        self.name = name


db.drop_all()


@app.route('/')
def index():
    return 'Hello, world!'


@app.route('/query')
def query():
    emp = Employee.query.join(Department, Employee.department == Department.id).with_entities(Employee.username,
                                                                                              Department.name).filter(
        Department.name == '研发部').all()
    return str(emp)


@app.route('/stat')
def stat():
    emp = Employee.query.join(Department, Employee.department == Department.id).with_entities(Department.name,db.func.count( Employee.id)).group_by(Department.name).all()
    return str(emp)


@app.route('/insert')
def insert():
    depts = ['研发部', '销售部', '财务部']
    for dept in depts:
        d = Department(name=dept)
        db.session.add(d)
    db.session.commit()
    for i in range(10):
        emp = Employee(username=f'员工{i}', password='123456', department=random.randint(1, 3))
        db.session.add(emp)
    db.session.commit()
    return '插入数据成功!'


if __name__ == '__main__':
    app.run(debug=True)
