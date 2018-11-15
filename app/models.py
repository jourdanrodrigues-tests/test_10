from core.exceptions import BadRequestError
from db.query import Model, Query


class RecipeQuery(Query):
    def create(self, **data):
        # TODO: Implement this in Postgres
        difficulty_choices = self.model.RECIPE_DIFFICULTIES_CHOICES
        if data.get('difficulty') not in difficulty_choices:
            first, last = difficulty_choices[0], difficulty_choices[-1]
            raise BadRequestError('Recipe difficulty should be between {} and {}'.format(first, last))
        super().create(**data)


class Recipe(Model):
    query_class = RecipeQuery
    fields = ['id', 'name', 'difficulty', 'vegetarian', 'preparation_time']

    RECIPE_DIFFICULTIES_CHOICES = [1, 2, 3]


class User(Model):
    fields = ['id']
