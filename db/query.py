from typing import Iterable

from core.environment import DB_DATA
from core.exceptions import ProgrammingError
from db.helpers import call_close, get_autocommit_connection

__all__ = [
    'Model',
    'Query',
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

    def _get_where_statement_and_values(self) -> tuple:
        fields = []
        values = []
        for field, value in self._where.items():
            if '__contains' in field:
                fields.append('{} like %s'.format(field.replace('__contains', '')))
                values.append('%{}%'.format(value))
            elif '__startswith' in field:
                fields.append('{} like %s'.format(field.replace('__startswith', '')))
                values.append('{}%'.format(value))
            elif '__endswith' in field:
                fields.append('{} like %s'.format(field.replace('__endswith', '')))
                values.append('%{}'.format(value))
            elif '__in' in field:
                fields.append('{} in %s'.format(field.replace('__in', '')))
                values.append('({})'.format(', '.join(value)))
            else:
                fields.append('{} = %s'.format(field))
                values.append(value)

        return ' where {};'.format(' and '.join(fields)), values

    def _fetch(self):
        query_string = 'select {} from "{}"'.format(
            ', '.join(self.model.fields),
            self.model.get_table_name(),
        )

        if self._where:
            where, values = self._get_where_statement_and_values()
            query_string += where
            self._run_query(query_string, values)
        else:
            self._run_query(query_string + ';')

    def _parse_entry_to_instance(self, entry: Iterable):
        return self.model(**{field: value for field, value in zip(self.model.fields, entry)})

    def filter(self, **kwargs):
        self._where = {**self._where, **kwargs}
        return self

    def fetch_all(self):
        self._fetch()
        return [self._parse_entry_to_instance(entry) for entry in self._cursor.fetchall()]

    def fetch_one(self):
        self._fetch()
        entry = self._cursor.fetchone()
        if entry is None:
            raise self.model.DoesNotExist
        return self._parse_entry_to_instance(entry)

    def create(self, **data):
        keys = data.keys()

        query_string = 'insert into "{}" ({}) values ({}) returning id;'.format(
            self.model.get_table_name(),
            ', '.join(keys),
            ', '.join(['%s' for _ in keys])
        )
        self._run_query(query_string, list(data.values()))
        created_id = self._cursor.fetchone()[0]
        return self.model(**{'id': created_id, **data})

    def update(self, **data):
        query_string = 'update "{}" set {}'.format(
            self.model.get_table_name(),
            ', '.join(['{} = %s'.format(key) for key in data.keys()]),
        )

        if self._where:
            where, values = self._get_where_statement_and_values()
            query_string += where
            values = list(data.values()) + values
        else:
            query_string += ';'
            values = data.values()

        self._run_query(query_string, values)
        return self._cursor.rowcount

    def delete(self, force=True):
        query_string = 'delete from "{}"'.format(self.model.get_table_name())
        if not self._where:
            if not force:
                raise ProgrammingError('Cannot delete without filtering or setting "force" to true.')
            self._run_query(query_string)
        else:
            where, values = self._get_where_statement_and_values()
            query_string += where
            self._run_query(query_string, values)

        return self._cursor.rowcount

    def _run_query(self, *args, **kwargs):
        self._connect()
        self._cursor.execute(*args, **kwargs)


class ModelMetaclass(type):
    @property
    def query(cls) -> Query:
        query_class = getattr(cls, 'query_class')  # Gets rid of warning
        return query_class(model=cls)


class Model(metaclass=ModelMetaclass):
    id = None
    query_class = Query

    def __init__(self, **kwargs):
        for field in self.fields:
            setattr(self, field, kwargs.get(field))

    @property
    def fields(self) -> Iterable:
        raise NotImplementedError()

    @classmethod
    def get_table_name(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self):
        return {field: getattr(self, field) for field in self.fields}

    class DoesNotExist(Exception):
        pass
