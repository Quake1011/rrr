import mysql.connector                  # ВСЕ
from mysql.connector import Error       # НУЖНЫЕ
from psycopg2 import OperationalError   # БИБЛИОТЕКИ

def create_connection(db_name, db_user, db_password, db_host, db_port): #функция выполнения подключения к базе
    connection = None #инициализация переменной как отсутствующее подключение
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        ) #использование библиотеки psycopg2
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection
    
def create_database(connection, query): #функция создания базы через аттрибут запроса "query"
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

create_database_query = "CREATE DATABASE db_newdb" #инициализация переменной, содержащей запрос на создание базы
create_database(connection, create_database_query) #использование вышеописанной функции
connection = create_connection("db_newdb", "user", "abc123", "127.0.0.1", "5432") #подключение 
#создание таблиц
#любой запрос в нашу базу осуществляется фунцией execute_query(connection, query)
create_users_table = "CREATE TABLE IF EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER, gender TEXT, nationality TEXT)"
create_posts_table = "CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id))"
create_comments_table = "CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, user_id INTEGER NOT NULL, post_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id))"
create_likes_table = "CREATE TABLE IF NOT EXISTS likes (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, post_id integer NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id))"
tables[4] = {create_users_table,create_posts_table,create_comments_table,create_likes_table}#инициализация массива с запросами
for i in range(0,4):
    execute_query(connection, tables[i])#цикл создания таблиц
    
#внесение данных в таблицу
create_user_data = "INSERT INTO users (name, age, gander, nationality) VALUES ('NAME', 25, 'm/f','COUNRTY'),('Alexandr',20,'m','RUS'),('Roman',20,'m','RUS')"
execute_query(connection, create_user_data)