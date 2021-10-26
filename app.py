##################################################################
#
#          Трекер задач
#       (12.08.) - (13.08)
#         ....askvart.....
##################################################################

import os
import datetime
from flask import Flask, g, request, render_template, flash, url_for, session
from sqlalchemy import create_engine, select, or_
from sqlalchemy.sql import func
from werkzeug.utils import redirect
from Model.tables import users, tasks, metadata

DATABASE = '/tmp/todo_002.db'
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')
STATIC_FOLDER = 'static'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'todo_002db')))

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
    '''Список пользователей'''
    db = get_db()
    query = select([users])
    r = db.execute(query)
    rows = r.fetchall()
    return rows

def get_users_one():
    '''заглушка'''
    db = get_db()
    query = select([users])
    r = db.execute(query)
    rows = r.fetchone()
    return rows[1]

def get_tasks_open():
    '''Список открытых задач'''
    db = get_db()
    query = select([tasks]).where(
        tasks.c.cancel_status == False,
        tasks.c.status == False,
    )
    r = db.execute(query)
    rows = r.fetchall()
    return rows

def get_tasks_take_work():
    '''Список взятых в работу задач'''
    db = get_db()
    query = select([tasks]).where(
        tasks.c.take_work_status == True,
        tasks.c.get_done_status == False,
    )
    r = db.execute(query)
    rows = r.fetchall()
    return rows

def get_tasks_archive():
    '''Список задач отправленных в архив(выполненные и отмененные)'''
    db = get_db()
    query = select([tasks]).where(
        or_(
            tasks.c.delete_status == True,
            tasks.c.cancel_status == True,
        )
    ).order_by(tasks.c.cancel_status)
    r = db.execute(query)
    rows = r.fetchall()
    return rows

def statistic_all_tasks():
    ''' Статистика всех заданий (на текущее время) '''
    db = get_db()
    cdb = [
        func.count(tasks.c.id)
    ]
    query = select(cdb)
    r = db.execute(query)
    rows = r.fetchone()
    return rows[0]

def statistic_cancel_tasks():
    ''' Статистика всех отмененных заданий (на текущее время)'''
    db = get_db()
    cdb = [
        func.count(tasks.c.id)
    ]
    query = select(cdb).where(
        tasks.c.cancel_status == True
    )
    r = db.execute(query)
    rows = r.fetchone()
    return rows[0]

def statistic_open_tasks():
    ''' Статистика всех открытых заданий (на текущее время)'''
    db = get_db()
    cdb = [
        func.count(tasks.c.id)
    ]
    query = select(cdb).where(
        tasks.c.cancel_status == False,
        tasks.c.status == False,
    )
    r = db.execute(query)
    rows = r.fetchone()
    return rows[0]

def statistic_take_work_tasks():
    ''' Статистика всех заданий находящихся в работе (на текущее время)'''
    db = get_db()
    cdb = [
        func.count(tasks.c.id)
    ]
    query = select(cdb).where(
        tasks.c.take_work_status == True,
        tasks.c.get_done_status == False,
    )
    r = db.execute(query)
    rows = r.fetchone()
    return rows[0]

def statistic_get_done_tasks():
    ''' Статистика всех выполненных заадний (на текущее время)'''
    db = get_db()
    cdb = [
        func.count(tasks.c.id)
    ]
    query = select(cdb).where(
        tasks.c.get_done_status == True
    )
    r = db.execute(query)
    rows = r.fetchone()
    return rows[0]

# Страничка статистики
@app.route('/statistics')
def statistics():
    '''стастистика '''
    return render_template("statistics.html",
                           count_all_tasks=statistic_all_tasks(),
                           count_done_tasks=statistic_get_done_tasks(),
                           count_all_cancel_tasks=statistic_cancel_tasks(),
                           count_all_open_tasks=statistic_open_tasks(),
                           count_take_work_tasks=statistic_take_work_tasks(),
                           )

##### Кнопка взять задание в работу
@app.route("/selecting/<int:task_id>")
def selecting(task_id):
    '''Кнопка взять в работу'''
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
        )
        db.execute(query2)
    return redirect(url_for("home"))

##### Кнопка задание выполнено
@app.route("/workdone/<int:task_id>")
def workdone(task_id):
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
            data_get_done=datetime.datetime.now(),
            get_done_status=True,
        )
        db.execute(query2)
    return redirect(url_for("home"))

#Страничка архива списка задач
@app.route('/tasksarchive')
def tasksarchive():
    '''открытые задания '''
    return render_template("tasks_archive.html", task_list=get_tasks_archive())

#Страничка списка открытых задач
@app.route('/tasksopen')
def tasksopen():
    '''открытые задания '''
    return render_template("tasks_open.html", task_list=get_tasks_open())

# Страничка списка взятых в работу
@app.route('/taskstakework')
def taskstakework():
    '''взятые в работу '''
    return render_template("tasks_take_work.html", task_list=get_tasks_take_work())

def get_task_list():
    '''Показать все доступные задачи'''
    db = get_db()
    query = select([tasks]).where(
        tasks.c.delete_status == False,
        tasks.c.cancel_status == False,
    )
    r = db.execute(query)
    rows = r.fetchall()
    return rows

@app.route('/', methods=['GET', 'POST'])
def home():
    '''Главная страница управление сессией'''
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'GET':
            return render_template("index.html", task_list=get_task_list(), data=get_users_one(), user_list=get_users())

def add_task():
    '''Процедура  для функции add()'''
    db = get_db()
    query = tasks.insert().values(
        title=request.form.get("title"),
        note=request.form.get("note"),
        status=False,
        data_create_task=datetime.datetime.now(),
        user_id=request.form.get("user_id"),
    )
    db.execute(query)

@app.route("/add", methods=["POST"])
def add():
    '''Добавить новое задание'''
    if request.method == "POST":
        if len(request.form['title']) > 5 and len(request.form['note']) > 10:
            add_task()
    return redirect(url_for("home"))

def select_task(task_id):
    '''Определяет запись в таблице для функций update() и delete()'''
    db = get_db()
    query = select([tasks]).where(
        tasks.c.id == task_id
    )
    r = db.execute(query)
    rows = r.fetchone()
    return rows

def update_task(task_id):
    '''Процедура для функции update()'''
    db = get_db()
    rows = select_task(task_id)
    if rows != None:
        query2 = tasks.update().where(
            tasks.c.id == task_id
        ).values(
            status=True
        )
        db.execute(query2)

@app.route("/update/<int:task_id>")
def update(task_id):
    '''Обновить статус задания на выполнено'''
    update_task(task_id)
    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>", methods=['GET', 'POST'])
def delete(task_id):
    '''Удалить задание из списка активных (переместить в архив)'''
    db = get_db()
    rows = select_task(task_id)
    if rows != None:
        query2 = tasks.update().where(
            tasks.c.id == task_id
        ).values(
            delete_status=True
        )
        db.execute(query2)

    return redirect(url_for("home"))

@app.route("/cancel/<int:task_id>", methods=['GET', 'POST'])
def cancel(task_id):
    '''Удалить задание'''
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
            cancel_status=True,
            data_cancel=datetime.datetime.now()
        )
        db.execute(query2)

    return redirect(url_for("home"))

def create_tables():
    '''запускается один раз, в случае обновления схемы таблиц,
     или создания новой БД. Запустить можно с консоли '''
    metadata.create_all(connect_db().engine)

def select_login_user(log, passw):
    '''Вспомогательная функция для функции login()'''
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

if __name__ == "__main__":
    app.run(debug=True, port=8000, host='127.0.0.1')
    
