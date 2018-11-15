class ProgrammingError(Exception):
    pass


class APIError(Exception):
    @property
    def message(self) -> str:
        raise NotImplementedError()

    @property
    def status_code(self) -> int:
        raise NotImplementedError()


class BadRequestError(APIError):
    status_code = 400
    message = None

    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop('message', args[0])
        super().__init__(*args, **kwargs)


class UnauthorizedError(APIError):
    status_code = 401
    message = 'Invalid authorization sent'
