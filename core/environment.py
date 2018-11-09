import os

__all__ = [
    'PORT',
]

PORT = os.getenv('PORT', 8080)
