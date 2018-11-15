from app.models import User


def authentication_required(view):
    def wrapper(request, *args, **kwargs):
        user_id = request.headers.get('Authorization')
        if not user_id:
            return {'detail': 'Invalid authorization sent'}, 401

        try:
            request.user = User.query.filter(id=user_id).fetch_one()
        except User.DoesNotExist:
            return {'detail': 'Invalid authorization sent'}, 401

        return view(request, *args, **kwargs)

    return wrapper


