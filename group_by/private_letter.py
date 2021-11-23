"""
# coding:utf-8
@Time    : 2021/11/23
@Author  : jiangwei
@File    : private_letter.py
@Desc    : private_letter
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func

from faker import Faker
import random
import datetime

username = 'jiangwei'
password = '1994124'
database = 'demo'
f = Faker(locale='zh_CN')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@localhost/{database}?charset=utf8'
app.config['SECRET_KEY'] = 'sfajn1314jnm14h1'
db = SQLAlchemy(app)


class PrivateMessage(db.Model):
    __tablename__ = 't_private_message'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.INTEGER, nullable=False)
    receiver_id = db.Column(db.INTEGER, nullable=False)
    content = db.Column(db.TEXT, nullable=False, default='')
    c_time = db.Column(db.DATETIME, default=datetime.datetime.now)


db.create_all()


@app.route('/')
def index():
    user_id = random.randint(1, 3)
    return render_template('index.html', user_id=user_id)


@app.route('/insert')
def insert():
    for i in range(10):
        pm = PrivateMessage(
            sender_id=random.randint(1, 20),
            receiver_id=random.randint(1, 3),
            content=f.sentence()
        )
        db.session.add(pm)
    db.session.commit()
    flash('插入数据成功!')
    return redirect(url_for('.index'))


@app.route('/insert/<user_id>')
def query(user_id):
    try:
        pms = PrivateMessage.query.\
            with_entities(PrivateMessage.sender_id,
                          func.any_value(PrivateMessage.content),
                          func.max(PrivateMessage.c_time)). \
            filter(PrivateMessage.receiver_id == user_id). \
            order_by(func.max(PrivateMessage.c_time).desc()). \
            group_by(PrivateMessage.sender_id).all()
    except Exception as e:
        pms = PrivateMessage.query.\
            with_entities(PrivateMessage.sender_id,
                          PrivateMessage.content,
                          func.max(PrivateMessage.c_time)).\
            filter(PrivateMessage.receiver_id == user_id).\
            order_by(func.max(PrivateMessage.c_time).desc()).\
            group_by(PrivateMessage.sender_id).all()
    return render_template('query.html', pms=pms, user_id=user_id)


if __name__ == '__main__':
    app.run(port=5005, debug=True)
