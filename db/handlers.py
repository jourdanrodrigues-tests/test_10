import psycopg2

from db.helpers import create_database_if_not_exists, get_autocommit_connection, call_close
from app.models import Model  # Importing directly from "db.query" causes the actual models not to be read


def setup_database(db_data):
    create_database_if_not_exists(db_data)

    for model in Model.__subclasses__():
        model.query.create_db_schema()


def drop_database(db_data):
    postgres_db_data = db_data.copy()
    postgres_db_data['dbname'] = 'postgres'

    connection = get_autocommit_connection(**postgres_db_data)
    cursor = connection.cursor()

    try:
        cursor.execute('DROP DATABASE {};'.format(db_data['dbname']))
    except psycopg2.OperationalError as exc:
        message = str(exc)
        if 'is being accessed by other users' not in message:
            raise exc
        print(message.capitalize(), ' Cannot drop it.')

    call_close(cursor, connection)
