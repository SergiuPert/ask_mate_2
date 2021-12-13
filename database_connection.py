import pymysql
import os
from dotenv import load_dotenv

load_dotenv()


def open_database():
    try:
        connection = pymysql.connect(
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            db=os.getenv("DB"),
        )
    except pymysql.DatabaseError as exception:
        print("Database connection problem")
        raise exception

    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        ret_value = function(cursor, *args, **kwargs)
        connection.commit()
        connection.close()
        return ret_value

    return wrapper
