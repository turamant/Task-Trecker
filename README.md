<h2>Task Trecker v.0.0.1</h2>
<p>Very simple task tracker.</p>
<p>In it, you can create tasks in work,</p>
<p>mark how to perform completed or canceled,</p>
<p>view the archive, view statistics.</p>

<h3>Requirements</h3>
 <li>Python3 (3.6-3.9)</li>
 <li>Flask</li>
 <li>SQLAlchemy Core</li>
 <li>SQLite</li>

   
<h3>Installation</h3>
 <li>python -m pip --upgrade pip</li>
 <li>python -m pip install pipenv</li>  
 <li>pipenv install -r requirements.txt</li>
   
<h3>Data base MariDB</h3>

<li>users</li>
<li>'id', Integer, primary_key=True, nullable=False</li>
<li>'login', String(100), unique=True, nullable=False</li>
<li>'password', String(100), nullable=False</li>
<li>'data_create_user', DateTime</li>
              

<li>tasks</li>
<li>'id', Integer, primary_key=True, nullable=False</li>
<li>'title', String(100), unique=True</li>
<li>'note', String(100), nullable=False</li>
<li>'status', Boolean, default=0</li>
<li>'data_create_task', DateTime</li>
<li>'data_take_work', DateTime</li>
<li>'take_work_status', Boolean, default=0</li>
<li>'data_get_done', DateTime</li>
<li>'get_done_status', Boolean, default=0</li>
<li>'delete_status', Boolean, default=0</li>
<li>'cancel_status', Boolean, default=0</li>
<li>'data_cancel', DateTime</li>
<li>'user_id', ForeignKey("users.id")</li>
                                                                         
<h3>Data base load dump</h3>
     <li>todo_002.db.sql</li>
     <li>tasks.json</li>
     <li>users.json</li>
     <li>todo_002.db</li>

<h3>How to use</h3>
 <li>python  app.py</li>

<h3>Tested on</h3>
    <li>Manjaro</li>
    <li>Debian</li>
    <li>Fedora</li>

<h3>Give it a Star</h3>
If you find this repo useful , 
give it a star so as many people can get to know it.


![alt text](screenshots/1.jpg "Описание будет тут")
![alt text](screenshots/2.jpg "Описание будет тут")
![alt text](screenshots/3.jpg "Описание будет тут")
![alt text](screenshots/4.jpg "Описание будет тут")

