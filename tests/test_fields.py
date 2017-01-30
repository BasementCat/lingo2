import re
import unittest
from datetime import date, datetime

import requests
import pytz

from lingo2 import fields
from lingo2.model import EmbeddedModel


class TestFields(unittest.TestCase):
    def test_field_default(self):
        f = fields.Field()
        self.assertIsNone(f.get_default())

        f = fields.Field(default='foo')
        self.assertEquals('foo', f.get_default())

        f = fields.Field(default=lambda: 'bar')
        self.assertEquals('bar', f.get_default())

    def test_listfield(self):
        f = fields.ListField(fields.IntField())
        self.assertEquals([1], f.serialize(['1']))
        self.assertEquals([1], f.deserialize('1'))

    def test_dictfield(self):
        f = fields.DictField(fields.IntField())
        self.assertEquals({'foo': 1}, f.serialize({'foo': '1'}))
        self.assertEquals({'foo': 1}, f.deserialize({'foo': '1'}))

    # No tests for StrField, IntField, FloatField (all behave as Field)

    def test_unicodefield(self):
        f = fields.UnicodeField()
        encoded = 'Testing \xc2\xab\xcf\x84\xce\xb1\xd0\x91\xd0\xac\xe2\x84\x93\xcf\x83\xc2\xbb: 1<2 & 4+1>3, now 20% off!'
        self.assertEquals(encoded, f.serialize(encoded.decode('utf-8')))
        self.assertEquals(encoded.decode('utf-8'), f.deserialize(encoded))

    def test_modelfield(self):
        class m(EmbeddedModel):
            mf = fields.IntField()

        f = fields.ModelField(m)

        self.assertEquals({'mf': 5}, f.serialize(m(mf=5)))
        self.assertEquals(5, f.deserialize({'mf': 5}).mf)

    def test_datefield(self):
        f = fields.DateField()
        self.assertEquals('2017-01-29', f.serialize(date(2017, 1, 29)))
        self.assertEquals(date(2017, 1, 29), f.deserialize('2017-01-29'))

    def test_datetimefield(self):
        f = fields.DateTimeField()
        self.assertEquals('2017-01-29T20:20:01.001234+00:00', f.serialize(datetime(2017, 1, 29, 20, 20, 1, 1234, pytz.timezone('UTC'))))
        self.assertEquals(datetime(2017, 1, 29, 20, 20, 1, 1234, pytz.timezone('UTC')), f.deserialize('2017-01-29T20:20:01.001234+00:00'))

        self.assertEquals('2017-01-29T20:20:01.001234-05:51', f.serialize(datetime(2017, 1, 29, 20, 20, 1, 1234, pytz.timezone('America/Chicago'))))
        self.assertEquals(datetime(2017, 1, 29, 20, 20, 1, 1234, pytz.timezone('America/Chicago')), f.deserialize('2017-01-29T20:20:01.001234-05:51'))
