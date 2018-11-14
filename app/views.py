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
    recipe_id = kwargs['id']
    try:
        return Recipe.query.filter(id=recipe_id).fetch_one()
    except Recipe.DoesNotExist:
        return {'detail': 'Recipe of ID {} does not exist.'.format(recipe_id)}, 404


def update_recipe(request, **kwargs):
    Recipe.query.filter(id=kwargs['id']).update(**request.data)
    return {**kwargs, **request.data}


def create_recipe(request):
    return Recipe.query.create(**request.data)


def delete_recipe(request, **kwargs):
    Recipe.query.filter(id=kwargs['id']).delete()
    return None, 204
