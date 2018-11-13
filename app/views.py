from app.models import Recipe

__all__ = [
    'update_recipe',
    'create_recipe',
    'get_recipe',
    'get_recipes',
    'delete_recipe',
]


def get_recipes(request, **kwargs):
    return Recipe().get_all()


def get_recipe(request, **kwargs):
    return Recipe().get_one(id=kwargs['id'])


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
