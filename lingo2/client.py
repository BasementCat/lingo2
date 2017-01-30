import threading

import requests
import purl


class Client(object):
    def __init__(self, uri=None, ssl=None, host=None, port=None, username=None, password=None, default_database=None):
        self.auth = None
        if uri:
            self.uri = str(purl.URL(uri, username='', password='', path='', fragment=''))
            uri = purl.URL(uri)
            if uri.username() or uri.password():
                self.auth = (uri.username() or '', uri.password() or '')
            self.default_database = uri.path().strip('/') or None
        else:
            self.uri = str(purl.URL(
                scheme='https' if ssl else 'http',
                host=host or 'localhost',
                port=port or 5984,
            ))
            if username or password:
                self.auth = (username or '', password or '')
            self.default_database = default_database

        self.uri = self.uri.rstrip('/')

        self.sessions = threading.local()

    @property
    def session(self):
        if not hasattr(self.sessions, 'session'):
            self.sessions.session = requests.Session()
        return self.sessions.session

    def request(self, method, path, *args, **kwargs):
        # TODO: take args better
        # TODO: handle errors specifically
        res = getattr(self.session, method.lower())(self.uri + path, *args, **kwargs)
        res.raise_for_status()
        return res

    def database(self, database_name=None):
        return Database(self, database_name or self.default_database)

    @property
    def version(self):
        return self.request('GET', '/').json()['version']

    @property
    def databases(self):
        return self.request('GET', '/_all_dbs').json()

    def __getitem__(self, key):
        return self.database(key)

    def __setitem__(self, key, value):
        # Nothing to do with the value right now
        return self.request('PUT', '/' + key).json()['ok']

    def __delitem__(self, key):
        return self.request('DELETE', '/' + key).json()['ok']


class Database(object):
    def __init__(self, client, database_name):
        self.client = client
        self.database_name = database_name

    def request(self, method, path, *args, **kwargs):
        return self.client.request(method, '/' + self.database_name + path)

    @property
    def props(self):
        return self.request('GET', '').json()

    # No magic methods here, since the _rev property is a requirement
