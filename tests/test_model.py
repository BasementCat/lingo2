import re
import unittest

import requests

from lingo2.model import Model


class TestModel(unittest.TestCase):
    def test_init_empty(self):
        pass
        # m = Model()
        # self.assertTrue(re.match(ur'^Model(.[a-f0-9]{16}){2}$', m._id))
        # self.assertIsNone(m._rev)
