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
    data = request.get_payload()
    Recipe.query.filter(id=kwargs['id']).update(**data)
    return {**kwargs, **data}


def create_recipe(request):
    data = request.get_payload()
    return Recipe.query.create(**data)


def delete_recipe(request, **kwargs):
    Recipe.query.filter(id=kwargs['id']).delete()
    return None, 204
