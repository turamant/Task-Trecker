##################################################################
#
#  Трекер задач
#       (12.08.)
#################################################################

import datetime
import os.path

from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, CheckConstraint, Boolean
from sqlalchemy import insert, select, update, delete
from flask import Flask, flash, render_template, request, redirect, url_for, g

from flask_login import LoginManager

# конфигурация приложения
DATABASE = '/tmp/todo_001.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'



app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'todo_001.db')))

#login_manager = LoginManager(app)

#Таблицы приложения
metadata = MetaData()
users = Table('users', metadata,
              Column('id', Integer(), primary_key=True, nullable=False),
              Column('login', String(100), unique=True, nullable=False),
              Column('password', String(100), nullable=False),
              Column('data_create_user', DateTime()),
              )
tasks = Table('tasks', metadata,
              Column('id', Integer(), primary_key=True, nullable=False),
              Column('title', String(100), unique=True),
              Column('note', String(100), nullable=False),
              Column('status', Boolean(), default=0),
              Column('data_create_todo', DateTime()),
              Column('user_id', ForeignKey("users.id")),
              )


def connect_db():
    '''Соединение с БД'''
    engine = create_engine('sqlite:///todo_001.db')
    conn = engine.connect()
    return conn

def get_db():
    '''Соединение с БД в момент запроса, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def home():
    '''Главная страница'''
    db = get_db()
    query = select([tasks])
    r = db.execute(query)
    rows = r.fetchall()
    return render_template("base.html", todo_list=rows)

@app.route("/add", methods=["POST"])
def add():
    '''Добавить задания'''
    db = get_db()
    if request.method == "POST":
        if len(request.form['title']) > 5 and len(request.form['note']) > 10:
            query = tasks.insert().values(
                title=request.form.get("title"),
                note=request.form.get("note"),
                status=False,
                data_create_todo=datetime.date.today()
            )
            db.execute(query)
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    '''Обновить статус на выполнено'''
    db = get_db()
    query = select([tasks]).where(
        tasks.c.id == todo_id
    )
    r = db.execute(query)
    rows = r.fetchone()
    if rows != None:
        query2 = tasks.update().where(
        tasks.c.id == todo_id
        ).values(
            status=True
        )
        db.execute(query2)
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>", methods=['GET', 'POST'])
def delete(todo_id):
    '''Удалить задание'''
    db = get_db()
    query = select([tasks]).where(
        tasks.c.id == todo_id
    )
    r = db.execute(query)
    rows = r.fetchone()
    if rows != None:
        query2 = tasks.delete().where(
            tasks.c.id == todo_id
        )
        db.execute(query2)

    return redirect(url_for("home"))

#Создаем таблицы(вызываем из консоли один раз)
def create_tables():
    metadata.create_all(connect_db().engine)



if __name__ == "__main__":
    app.run(debug=True)
