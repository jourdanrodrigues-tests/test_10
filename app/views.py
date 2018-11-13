from app.models import Recipe

__all__ = [
    'update_recipe',
    'create_recipe',
    'get_record',
    'get_recipes',
    'delete_recipe',
]

records = {}


def get_recipes(request, **kwargs):
    return Recipe().get_all()


def get_record(request, **kwargs):
    key = request.path[8:]
    return (records[key], 200) if key in records else (None, 404)


def update_recipe(request, **kwargs):
    data = {**kwargs, **request.get_payload()}
    recipe = Recipe(**data)
    recipe.update()
    return recipe.serialize()


def create_recipe(request, **kwargs):
    data = {**kwargs, **request.get_payload()}
    recipe = Recipe(**data)
    recipe.create()
    return recipe.serialize()


def delete_recipe(request, **kwargs):
    Recipe(id=kwargs['id']).delete()
    return None, 204
