from typing import Iterable

from core.db.query import Query


class Model:
    id = None
    query_class = Query

    def persist(self, query_string: str, values: Iterable) -> None:
        query = self.query_class()
        query.prepare(query_string, values)
        query.execute()

    @property
    def _fields(self) -> Iterable:
        raise NotImplementedError()

    def get_table_name(self):
        return self.__class__.__name__.lower()

    def get_all(self):
        query = self.query_class()
        query.prepare('select {} from {};'.format(
            ', '.join(self._fields),
            self.get_table_name(),
        ))
        return [
            {field: value for field, value in zip(self._fields, entry)}
            for entry in query.fetch_all()
        ]

    def create(self):
        keys, values = self._get_keys_values()
        query_string = 'insert into {} ({}) values ({});'.format(
            self.get_table_name(),
            ', '.join(keys),
            ', '.join(['%s' for _ in values])
        )
        self.persist(query_string, values)

    def update(self):
        keys, values = self._get_keys_values()
        query_string = 'update {} set {} where id = (%s);'.format(
            self.get_table_name(),
            ', '.join(['{} = %s'.format(key) for key in keys]),
        )
        values.append(self.id)
        self.persist(query_string, values)

    def delete(self):
        query_string = 'delete from {} where id = %s;'.format(self.get_table_name())
        self.persist(query_string, (self.id,))

    def _get_keys_values(self):
        keys = []
        values = []
        for field in self._fields:
            if field == 'id':
                continue
            keys.append(field)
            values.append(getattr(self, field))

        return keys, values


class Recipe(Model):
    _fields = ['id', 'name', 'difficulty', 'vegetarian', 'preparation_time']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.difficulty = kwargs.get('difficulty')
        self.vegetarian = kwargs.get('vegetarian')
        self.preparation_time = kwargs.get('preparation_time')
