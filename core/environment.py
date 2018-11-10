import os
import re

__all__ = [
    'PORT',
    'DB_DATA',
]

PORT = os.getenv('PORT', 8080)

db_match = re.match(
    r'\w+://(?P<user>\w+)(:(?P<password>\w+))@(?P<host>\w+)(:(?P<port>\d+))?/(?P<dbname>\w+)',
    os.getenv('DATABASE_URL', ''),
)
if db_match:
    DB_DATA = db_match.groupdict()
else:
    raise EnvironmentError('Variable "DATABASE_URL" is required in the environment')
