from socket import socket
from threading import Thread

import pytest

from server import get_http_server


def get_available_port() -> int:
    s = socket()
    s.bind(('', 0))
    return s.getsockname()[1]


PORT = get_available_port()
server = get_http_server(PORT)


@pytest.fixture(scope='session')
def server_host():
    return 'http://localhost:{}'.format(PORT)


@pytest.fixture(scope='session', autouse=True)
def setup_server():
    Thread(target=server.serve_forever).start()


def pytest_sessionfinish():
    server.shutdown()
