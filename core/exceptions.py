class ProgrammingError(Exception):
    pass


class APIError(Exception):
    message = ''

    @property
    def status_code(self) -> int:
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop('message', self.message)
        super().__init__(*args, **kwargs)


class BadRequestError(APIError):
    status_code = 400


class UnauthorizedError(APIError):
    status_code = 401
    message = 'Authorization not sent or invalid.'


class NotFoundError(APIError):
    status_code = 404
    message = 'Not found.'
