class ProgrammingError(Exception):
    pass


class APIError(Exception):
    message = ''

    @property
    def status_code(self) -> int:
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop('message', args[0])
        super().__init__(*args, **kwargs)


class BadRequestError(APIError):
    status_code = 400


class UnauthorizedError(APIError):
    status_code = 401
    message = 'Invalid authorization sent.'


class NotFoundError(APIError):
    status_code = 404
    message = 'Not found.'
