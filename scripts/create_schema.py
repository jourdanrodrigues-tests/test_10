import os
import re
import sys

import psycopg2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR])

from app.models import Recipe, Rating, User
from core.environment import DB_DATA
from db.helpers import get_autocommit_connection, call_close


def handle_db_creation_error(exception):
    message = str(exception)
    database_exists = re.search(r'already exists', message, re.IGNORECASE)
    if database_exists:
        print(message.capitalize())
    else:
        raise exception


def create_database_if_not_exists():
    db_data = {**DB_DATA, 'dbname': 'postgres'}
    connection = get_autocommit_connection(**db_data)
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE DATABASE {};'.format(DB_DATA['dbname']))
    except psycopg2.ProgrammingError as exc:
        handle_db_creation_error(exc)
    finally:
        call_close(cursor, connection)


def create_db_schemas(*args):
    for model in args:
        model.query.create_db_schema()


if __name__ == '__main__':
    create_database_if_not_exists()
    create_db_schemas(Recipe, User, Rating)
