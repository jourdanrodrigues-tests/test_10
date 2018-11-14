from typing import Iterable

from core.environment import DB_DATA
from core.exceptions import ProgrammingError
from db.helpers import call_close, get_autocommit_connection

__all__ = [
    'Model',
]


class DBConn:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def _connect(self):
        if not self._has_connection():
            self._connection = get_autocommit_connection(**DB_DATA)
            self._cursor = self._connection.cursor()

    def _has_connection(self):
        return self._connection and self._cursor

    def _close_connection(self):
        if self._has_connection():
            call_close(self._cursor, self._connection)

    def __del__(self):
        self._close_connection()


class Query(DBConn):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self._where = {}

    def _get_where_statement(self):
        where_clause = ' and '.join(
            ['{} = %s'.format(field) for field in self._where.keys()],
        )
        return ' where {};'.format(where_clause)

    def _fetch(self):
        query_string = 'select {} from {}'.format(
            ', '.join(self.model.fields),
            self.model.get_table_name(),
        )

        if self._where:
            query_string += self._get_where_statement()
            self._run_query(query_string, list(self._where.values()))
        else:
            self._run_query(query_string + ';')

    def filter(self, **kwargs):
        self._where = {**self._where, **kwargs}
        return self

    def fetch_all(self):
        self._fetch()
        return [
            {field: value for field, value in zip(self.model.fields, entry)}
            for entry in self._cursor.fetchall()
        ]

    def fetch_one(self):
        self._fetch()
        entry = self._cursor.fetchone()
        if entry is None:
            raise self.model.DoesNotExist
        return {field: value for field, value in zip(self.model.fields, entry)}

    def create(self, **data):
        keys = []
        values = []
        for field, value in data.items():
            if field == 'id':
                continue
            keys.append(field)
            values.append(value)

        query_string = 'insert into {} ({}) values ({}) returning id;'.format(
            self.model.get_table_name(),
            ', '.join(keys),
            ', '.join(['%s' for _ in keys])
        )
        self._run_query(query_string, values)
        created_id = self._cursor.fetchone()[0]
        return {'id': created_id, **data}

    def update(self, **data):
        query_string = 'update {} set {}'.format(
            self.model.get_table_name(),
            ', '.join(['{} = %s'.format(key) for key in data.keys()]),
        )

        if self._where:
            query_string += self._get_where_statement()
            values = list(data.values()) + list(self._where.values())
        else:
            query_string += ';'
            values = data.values()

        self._run_query(query_string, values)
        return self._cursor.rowcount

    def delete(self, force=True):
        query_string = 'delete from {}'.format(self.model.get_table_name())
        if not self._where:
            if not force:
                raise ProgrammingError('Cannot delete without filtering or setting "force" to true.')
            self._run_query(query_string)
        else:
            query_string += self._get_where_statement()
            self._run_query(query_string, list(self._where.values()))

        return self._cursor.rowcount

    def _run_query(self, *args, **kwargs):
        self._connect()
        self._cursor.execute(*args, **kwargs)


class ModelMetaclass(type):
    @property
    def query(cls) -> Query:
        return Query(model=cls)


class Model(metaclass=ModelMetaclass):
    id = None

    @property
    def fields(self) -> Iterable:
        raise NotImplementedError()

    @classmethod
    def get_table_name(cls) -> str:
        return cls.__name__.lower()

    class DoesNotExist(Exception):
        pass
