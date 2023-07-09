"""
coding:utf-8
file: _init__.py
@time: 2023/7/9 8:46
@desc:
"""
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from faker import Faker
import random

fake = Faker(locale='zh_CN')

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class BaseColumn:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update_or_insert(cls, condition: tuple, **kwargs):
        """
        更新已有数据或者插入新的数据

        :param condition: 查询条件
        :param kwargs: 需要更新或者插入的字段
        :return: 类实例对象
        """
        existed = cls.query.filter(*condition)
        if existed.first():
            existed.update(kwargs)
            existed = existed.first()
        else:
            existed = cls(**kwargs)
            db.session.add(existed)
        db.session.commit()
        return existed


class Music(BaseColumn, db.Model):
    __tablename__ = 't_music'

    name = db.Column(db.String(512), default='', comment='歌曲名称')
    author = db.Column(db.String(512), default='', comment='歌手名')


class Video(BaseColumn, db.Model):
    __tablename__ = 't_video'

    name = db.Column(db.String(512), default='', comment='电影名称')
    director = db.Column(db.String(512), default='', comment='电影导演')


db.drop_all()
db.create_all()


@app.route('/')
def index():
    return render_template(
        'index.html',
        musics=Music.query.all(),
        videos=Video.query.all()
    )


@app.route('/save')
def save():
    name = fake.catch_phrase()
    director = fake.name()
    obj = random.choice([1, 2])
    if obj == 1:
        video = Video.update_or_insert(Video.name == name, name=name, director=director)
        video.save()
    else:
        music = Music(name=name, author=director)
        music.save()

    return redirect('/')


@app.route('/delete/<id>')
def delete(id):
    if request.args.get('type') == 'video':
        v = Video.query.get(id)
        v.delete()
    else:
        m = Music.query.get(id)
        m.delete()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
