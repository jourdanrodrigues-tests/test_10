import psycopg2


__all__ = [
    'call_close',
    'get_autocommit_connection',
]


def call_close(*args) -> None:
    for arg in args:
        arg.close()


def get_autocommit_connection(**kwargs):
    conn = psycopg2.connect(**kwargs)
    conn.autocommit = True
    return conn
