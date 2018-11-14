from db.query import Model


class Recipe(Model):
    fields = ['id', 'name', 'difficulty', 'vegetarian', 'preparation_time']

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.difficulty = kwargs.get('difficulty')
        self.vegetarian = kwargs.get('vegetarian')
        self.preparation_time = kwargs.get('preparation_time')
