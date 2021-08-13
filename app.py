##################################################################
#
#  Трекер задач
#       (12.08.)
#################################################################

import datetime
from flask import Flask, g, request, render_template, flash, url_for, session
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine, select
from werkzeug.utils import redirect
import os

DATABASE = '/tmp/todo_002.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'todo_002.db')))

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
              Column('user_id', ForeignKey("users.id")),
              )

task_status = Table('task_status', metadata,
                    Column('task_id', ForeignKey("tasks.id"), primary_key=True),
                    Column('status', Boolean(), default=0),
                    Column('data_create_task', DateTime()),
                    Column('data_take_work', DateTime()),
                    Column('take_work_status', Boolean(), default=0),
                    Column('data_get_done', DateTime()),
                    Column('get_done_status', Boolean(), default=0),
                    )


def connect_db():
    '''Соединение с БД'''
    engine = create_engine('sqlite:///todo_002.db')
    conn = engine.connect()
    return conn

def get_db():
    '''Соединение с БД , если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

def get_users():
    db = get_db()
    query = select([users])
    r = db.execute(query)
    rows = r.fetchall()
    return rows

def get_tasks_open():
    db = get_db()
    query = select([tasks]).where(
        tasks.c.status == 0
    )
    r = db.execute(query)
    rows = r.fetchall()
    return rows

@app.route("/selecting/<int:task_id>")
def selecting(task_id):
    '''Обновить статус на выполнено'''
    db = get_db()
    query = select([tasks]).where(
        tasks.c.id == task_id
    )
    r = db.execute(query)
    rows = r.fetchone()

    if rows != None:
        query2 = tasks.update().where(
        tasks.c.id == task_id
        ).values(
            data_take_work=datetime.datetime.now(),
            take_work_status=True,
            get_done_status=False,
        )
        db.execute(query2)
    return redirect(url_for("home"))


@app.route('/', methods=['GET', 'POST'])
def home():
    '''Главная страница
    Управление сессией'''
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'GET':
            db = get_db()
            query = select([tasks])
            r = db.execute(query)
            rows = r.fetchall()
            return render_template("index.html", task_list=rows, data=get_users(), user_list=get_users())

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
                data_create_task=datetime.datetime.now(),
                data_take_work=datetime.datetime.now(),
                data_get_done=datetime.datetime.now(),
                user_id=request.form.get("user_id"),
            )
            db.execute(query)
    return redirect(url_for("home"))

@app.route("/update/<int:task_id>")
def update(task_id):
    '''Обновить статус на выполнено'''
    db = get_db()
    query = select([tasks]).where(
        tasks.c.id == task_id
    )
    r = db.execute(query)
    rows = r.fetchone()
    if rows != None:
        query2 = tasks.update().where(
        tasks.c.id == task_id
        ).values(
            status=True
        )
        db.execute(query2)
    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>", methods=['GET', 'POST'])
def delete(task_id):
    '''Удалить задание'''
    db = get_db()
    query = select([tasks]).where(
        tasks.c.id == task_id
    )
    r = db.execute(query)
    rows = r.fetchone()
    if rows != None:
        query2 = tasks.delete().where(
            tasks.c.id == task_id
        )
        db.execute(query2)

    return redirect(url_for("home"))

def create_tables():
    metadata.create_all(connect_db().engine)

@app.route('/tasksopen')
def tasksopen():
    '''открытые задания '''
    return render_template("tasks_open.html", task_list=get_tasks_open())

def select_login_user(log, passw):
    db = get_db()
    query = select([users]).where(
        users.c.login == log).where(
        users.c.password == passw
    )
    r = db.execute(query)
    login = r.first()
    return login

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Login Form'''
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login1 = request.form['login']
        password = request.form['password']
        login = select_login_user(login1, password)
        if login is not None:
            session['logged_in'] = True
            return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    db = get_db()
    if request.method == 'POST':
        query = users.insert().values(
            login=request.form.get("login"),
            password=request.form.get("password"),
            data_create_user=datetime.datetime.now(),
            )
        db.execute(query)
        return render_template('login.html')
    return render_template('register.html')

@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


#metadata.create_all(connect_db().engine)
if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='127.0.0.1')
