import os

PORT = os.getenv('PORT', 8000)
STACK = os.getenv('STACK', 'local')
DEBUG = os.getenv('DEBUG', False)
COOKIE_SECRET = os.getenv('COOKIE_SECRET', 'super secret!')
DB_HOST = os.getenv('DB_HOST',  'localhost')
DB_PORT = os.getenv('DB_PORT', '9200')


class SimpleMultiDict(dict):
    def getlist(self, key):
        return self[key]

    def __repr__(self):
        return type(self).__name__ + '(' + dict.__repr__(self) + ')'