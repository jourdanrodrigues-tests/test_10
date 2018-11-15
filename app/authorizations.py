from app.models import User
from core.exceptions import UnauthorizedError


def authentication_required(view):
    def wrapper(request, *args, **kwargs):
        user_id = request.headers.get('Authorization')
        if not user_id:
            raise UnauthorizedError()

        try:
            request.user = User.query.filter(id=user_id).fetch_one()
        except User.DoesNotExist:
            raise UnauthorizedError()

        return view(request, *args, **kwargs)

    return wrapper
