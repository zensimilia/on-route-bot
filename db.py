import os
import sqlite3
from sqlite3 import Error
from time import ctime
from dotenv import load_dotenv

# Initialize environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DB_FILE = os.getenv("DB_FILE", 'data.sqlite')


def post_sql_query(sql_query):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            pass
        result = cursor.fetchall()
        return result if result else cursor.lastrowid


def create_tables():
    users_query = '''CREATE TABLE IF NOT EXISTS USERS 
                        (id INTEGER PRIMARY KEY NOT NULL,
                        username TEXT,
                        reg_date TEXT);'''
    post_sql_query(users_query)


def register_user(user, username):
    user_check_query = f'SELECT * FROM USERS WHERE id = {user};'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO USERS (id, username, reg_date) VALUES ({user}, "{username}", "{ctime()}");'
        return post_sql_query(insert_to_db_query)
