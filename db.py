import sqlite3
from time import ctime
from config import Config

DB_FILE = Config.DB_FILE


def post_sql_query(sql_query):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except sqlite3.Error:
            pass
        result = cursor.fetchall()
        return result if result else cursor.lastrowid


def create_tables():
    with open('schema.sql', 'r') as f:
        schema = f.read()
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.executescript(schema)
        except sqlite3.Error:
            pass


def register_user(user_id, username):
    user_check_query = f'SELECT * FROM USERS WHERE user_id = {user_id};'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO USERS (user_id, username, reg_date) VALUES ({user_id}, "{username}", "{ctime()}");'
        return post_sql_query(insert_to_db_query)


def add_route(user_id, url, name, is_active=1):
    insert_to_db_query = f'INSERT INTO ROUTES (user_id, url, name, is_active) VALUES ({user_id}, "{url}", "{name}", {is_active});'
    return post_sql_query(insert_to_db_query)


def get_routes(user_id, route_id=None):
    get_routes_query = f'SELECT * FROM ROUTES WHERE user_id = {user_id};'
    if route_id:
        get_routes_query = f'SELECT * FROM ROUTES WHERE route_id = {route_id};'
    return post_sql_query(get_routes_query)


def get_user_timezone(user_id):
    get_timezone_query = f'SELECT timezone FROM USERS WHERE user_id = {user_id};'
    timezone = post_sql_query(get_timezone_query)
    return timezone if timezone else None


def add_user_timezone(user_id, timezone):
    add_timezone_query = f'UPDATE USERS SET timezone = "{timezone}" WHERE user_id = {user_id};'
    return post_sql_query(add_timezone_query)
