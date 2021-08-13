from sqlalchemy import MetaData, Table, Column, Integer, String, \
    DateTime, Boolean, ForeignKey

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
              Column('data_create_task', DateTime()),

              Column('data_take_work', DateTime()),
              Column('take_work_status', Boolean(), default=0),
              Column('data_get_done', DateTime()),
              Column('get_done_status', Boolean(), default=0),
              Column('delete_status', Boolean(), default=0),
              Column('cancel_status', Boolean(), default=0),
              Column('data_cancel', DateTime()),
              Column('user_id', ForeignKey("users.id")),
              )
