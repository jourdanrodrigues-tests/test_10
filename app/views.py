from app.models import Recipe

__all__ = [
    'update_recipe',
    'create_recipe',
    'get_record',
    'get_records',
    'delete_recipe',
]

records = {}


def get_records(request, **kwargs):
    return records


def get_record(request, **kwargs):
    key = request.path[8:]
    return (records[key], 200) if key in records else (None, 404)


def update_recipe(request, **kwargs):
    data = {**kwargs, **request.get_payload()}
    Recipe(**data).update()
    return data


def create_recipe(request, **kwargs):
    data = {**kwargs, **request.get_payload()}
    Recipe(**data).create()
    return data


def delete_recipe(request, **kwargs):
    Recipe(id=kwargs['id']).delete()
    return None, 204
