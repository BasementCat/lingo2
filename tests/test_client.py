import re
import unittest

import requests

from lingo2.client import Client


class TestClient(unittest.TestCase):
    def test_init_empty(self):
        cl = Client()
        self.assertEqual('http://localhost:5984', cl.uri)
        self.assertIsNone(cl.default_database)
        self.assertIsNone(cl.auth)

    def test_init_uri_basic(self):
        cl = Client('https://host:1234/')
        self.assertEqual('https://host:1234', cl.uri)
        self.assertIsNone(cl.default_database)
        self.assertIsNone(cl.auth)

    def test_init_uri_ext(self):
        cl = Client('https://user:pass@host:1234/foo')
        self.assertEqual('https://host:1234', cl.uri)
        self.assertEqual('foo', cl.default_database)
        self.assertEqual(('user', 'pass'), cl.auth)

    def test_init_kwargs(self):
        cl = Client(ssl=True, host='host', port=1234, username='user', password='pass', default_database='foo')
        self.assertEqual('https://host:1234', cl.uri)
        self.assertEqual('foo', cl.default_database)
        self.assertEqual(('user', 'pass'), cl.auth)

    def test_version(self):
        cl = Client()
        self.assertTrue(re.match(ur'^[\d.]+$', cl.version))

    def test_modify_db(self):
        cl = Client()
        self.assertFalse('unittest' in cl.databases)
        cl['unittest'] = True
        self.assertTrue('unittest' in cl.databases)
        del cl['unittest']
        self.assertFalse('unittest' in cl.databases)

    def test_duplicate_db(self):
        cl = Client()
        cl['unittest'] = True
        with self.assertRaisesRegexp(requests.HTTPError, '412'):
            cl['unittest'] = True
        del cl['unittest']

    def test_missing_db(self):
        cl = Client()
        with self.assertRaisesRegexp(requests.HTTPError, '404'):
            del cl['unittest']


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.cl = Client()
        try:
            del self.cl['unittest']
        except:
            pass
        self.cl['unittest'] = True

    @classmethod
    def tearDownClass(self):
        try:
            del self.cl['unittest']
        except:
            pass

    def test_props(self):
        self.assertEqual('unittest', self.cl['unittest'].props['db_name'])
