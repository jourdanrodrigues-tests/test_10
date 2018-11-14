from unittest.mock import Mock

from core import RequestHandler


class TestGetQueryParams:
    def test_when_request_has_path_with_query_params_returns_parsed_to_dict(self):
        request_handler = Mock(spec=RequestHandler, path='/?a=1&b=2')

        # noinspection PyCallByClass,PyTypeChecker
        assert RequestHandler.get_query_params(request_handler) == {'a': '1', 'b': '2'}

    def test_when_request_has_path_with_array_in_query_params_returns_parsed_to_dict(self):
        request_handler = Mock(spec=RequestHandler, path='/?a=1&b=2&b=3')

        # noinspection PyCallByClass,PyTypeChecker
        assert RequestHandler.get_query_params(request_handler) == {'a': '1', 'b': ['2', '3']}

    def test_when_request_has_path_without_query_params_returns_empty_dict(self):
        request_handler = Mock(spec=RequestHandler, path='/')

        # noinspection PyCallByClass,PyTypeChecker
        assert RequestHandler.get_query_params(request_handler) == {}
