import re
import unittest

import requests

from lingo2.client import Client
from lingo2.model import EmbeddedModel, Model
from lingo2 import fields


class TestModel(unittest.TestCase):
    def test_default(self):
        class m(EmbeddedModel):
            f = fields.IntField(default=5)

        self.assertEquals(5, m().f)
        self.assertEquals(7, m(f=7).f)

    def test_init_empty(self):
        m = Model()
        self.assertTrue(re.match(ur'^Model(.[a-f0-9]{16}){2}$', m._id))
        self.assertIsNone(m._rev)

    def test_save_load(self):
        class m(Model):
            f = fields.IntField()

        cl = Client(default_database='unittest')
        with cl:
            instance = m(f=25)
            instance.save()

            self.assertEquals(25, m.get(instance._id).f)
