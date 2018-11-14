from app.models import Recipe

__all__ = [
    'update_recipe',
    'create_recipe',
    'get_recipe',
    'get_recipes',
    'delete_recipe',
]


def get_recipes(request, **kwargs):
    return Recipe.query.fetch_all()


def get_recipe(request, **kwargs):
    return Recipe.query.filter(id=kwargs['id']).fetch_one()


def update_recipe(request, **kwargs):
    Recipe.query.filter(id=kwargs['id']).update(**request.data)
    return {**kwargs, **request.data}


def create_recipe(request):
    return Recipe.query.create(**request.data)


def delete_recipe(request, **kwargs):
    Recipe.query.filter(id=kwargs['id']).delete()
    return None, 204
