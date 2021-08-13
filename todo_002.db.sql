BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"login"	VARCHAR(100) NOT NULL,
	"password"	VARCHAR(100) NOT NULL,
	"data_create_user"	DATETIME,
	UNIQUE("login"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "tasks" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(100),
	"note"	VARCHAR(100) NOT NULL,
	"status"	BOOLEAN,
	"data_create_task"	DATETIME,
	"data_take_work"	DATETIME,
	"take_work_status"	BOOLEAN,
	"data_get_done"	DATETIME,
	"get_done_status"	BOOLEAN,
	"delete_status"	BOOLEAN,
	"cancel_status"	BOOLEAN,
	"data_cancel"	DATETIME,
	"user_id"	INTEGER,
	UNIQUE("title"),
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	PRIMARY KEY("id")
);
INSERT INTO "users" ("id","login","password","data_create_user") VALUES (1,'admin','1',NULL);
INSERT INTO "users" ("id","login","password","data_create_user") VALUES (2,'user1','1','2021-08-14 00:43:19.799785');
INSERT INTO "users" ("id","login","password","data_create_user") VALUES (3,'python','1','2021-08-14 00:43:50.831838');
INSERT INTO "users" ("id","login","password","data_create_user") VALUES (4,'van rossum','1','2021-08-14 00:44:30.166797');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (1,'Первое задание ','Написать программу Task Trecker',1,'2021-08-14 00:46:01.146376','2021-08-14 00:57:44.880354',1,'2021-08-14 00:50:21.157599',1,1,0,NULL,'admin');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (2,'Второе задание','Нарисовать натюрморт',1,'2021-08-14 00:46:22.293804','2021-08-14 00:51:11.328481',1,'2021-08-14 00:57:35.618838',1,1,0,NULL,'user1');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (3,'Третий задание','Прочитать статью о Python',1,'2021-08-14 00:46:49.133885','2021-08-14 00:49:33.874793',1,'2021-08-14 00:58:17.145808',1,1,0,NULL,'python');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (4,'Четвертое задание','Пробежать марафон 5 километров',0,'2021-08-14 00:47:35.045013',NULL,0,NULL,0,0,1,'2021-08-14 00:49:55.406775','van rossum');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (5,'Шестое задание','Повернуть реки на восток',1,'2021-08-14 00:48:28.484457','2021-08-14 00:49:43.798559',1,'2021-08-14 00:57:51.914916',1,1,0,NULL,'user1');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (6,'Седьмое задание ','просто выполнить нужно его',1,'2021-08-14 00:59:00.615611','2021-08-14 00:59:12.380710',1,'2021-08-14 00:59:21.959514',1,1,0,NULL,'van rossum');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (7,'Шестая задача','Самая простая задача - выучить теорему Фермадоказать теорему Ферма',1,'2021-08-14 01:00:23.272424','2021-08-14 01:01:25.382085',1,'2021-08-14 01:01:54.422013',1,1,0,NULL,'user1');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (8,'Десятое задание ','Отжаться от пола на кулаках',1,'2021-08-14 01:00:53.016270','2021-08-14 01:01:38.876168',1,'2021-08-14 01:01:58.159877',1,1,0,NULL,'user1');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (9,'Двадцать первое задание ','Придумайте сами, что хотите сделать',1,'2021-08-14 01:02:45.803240','2021-08-14 01:03:27.786907',1,'2021-08-14 01:04:18.677844',1,0,0,NULL,'python');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (10,'Двадцать второе задание ','Приготовить вкусный завтрак',0,'2021-08-14 01:03:16.301601',NULL,0,NULL,0,0,0,NULL,'user1');
INSERT INTO "tasks" ("id","title","note","status","data_create_task","data_take_work","take_work_status","data_get_done","get_done_status","delete_status","cancel_status","data_cancel","user_id") VALUES (11,'Двадцать третье задание ','Посчитать звезды на небе',0,'2021-08-14 01:04:07.026713','2021-08-14 01:04:41.462510',1,NULL,0,0,0,NULL,'python');
COMMIT;
