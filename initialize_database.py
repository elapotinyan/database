import psycopg2
from psycopg2 import sql

# Параметры подключения к серверу PostgreSQL
db_host = 'localhost'
db_port = '5432'
db_user = 'postgres'  # Пользователь для подключения
db_password = '1111'  # Ваш пароль
new_db_name = 'geograph_db'  # Имя новой базы данных
owner = 'postgres'  # Пользователь-владелец базы данных

# Подключаемся к PostgreSQL (без указания базы данных для создания новой)
conn = psycopg2.connect(
    dbname='postgres',
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

# Включаем режим автокоммита для выполнения CREATE DATABASE
conn.autocommit = True

# Создаем курсор для выполнения SQL-запросов
cur = conn.cursor()

# Создание новой базы данных
cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))

# Установка владельца базы данных
cur.execute(sql.SQL("ALTER DATABASE {} OWNER TO {}").format(
    sql.Identifier(new_db_name),
    sql.Identifier(owner)
))

# Закрытие соединения и курсора
cur.close()
conn.close()

print(f"База данных '{new_db_name}' успешно создана и владельцем установлено '{owner}'.")
