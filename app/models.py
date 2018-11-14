from typing import Iterable

from core.db.query import Query


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


class Recipe(Model):
    fields = ['id', 'name', 'difficulty', 'vegetarian', 'preparation_time']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.difficulty = kwargs.get('difficulty')
        self.vegetarian = kwargs.get('vegetarian')
        self.preparation_time = kwargs.get('preparation_time')
