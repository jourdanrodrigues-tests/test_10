from core.exceptions import BadRequestError
from db.query import Model, Query


class RecipeQuery(Query):
    def create(self, **data):
        # TODO: Implement this in Postgres
        difficulty_choices = self.model.DIFFICULTIES_CHOICES

        if data.get('difficulty') not in difficulty_choices:
            first, last = difficulty_choices[0], difficulty_choices[-1]
            raise BadRequestError('Recipe difficulty should be between {} and {}'.format(first, last))

        return super().create(**data)


class Recipe(Model):
    query_class = RecipeQuery
    fields = ['id', 'name', 'difficulty', 'vegetarian', 'preparation_time']

    DIFFICULTIES_CHOICES = [1, 2, 3]


class User(Model):
    fields = ['id']


class RatingQuery(Query):
    def create(self, **data):
        # TODO: Implement this in Postgres
        rating_choices = self.model.RATING_CHOICES

        if data.get('value') not in rating_choices:
            first, last = rating_choices[0], rating_choices[-1]
            raise BadRequestError('Rating value should be between {} and {}'.format(first, last))

        return super().create(**data)


class Rating(Model):
    query_class = RatingQuery
    fields = ['id', 'recipe_id', 'value']

    RATING_CHOICES = [1, 2, 3, 4, 5]
