import time
import os
import binascii

from client import Client, Database
import fields


class EmbeddedModel(object):
    @classmethod
    def _all_bases(self):
        out = []
        queue = [self]
        while queue:
            cls = queue.pop()
            out.append(cls)
            queue += list(cls.__bases__)
        return out

    @classmethod
    def iterfields(self):
        # TODO: cache this
        for cls in self._all_bases():
            for field_name, field_instance in vars(cls).items():
                if isinstance(field_instance, fields.Field):
                    yield field_name, field_instance

    def __init__(self, **kwargs):
        for field_name, field_instance in self.iterfields():
            if field_name in kwargs:
                setattr(self, field_name, field_instance.deserialize(kwargs[field_name]))
            else:
                setattr(self, field_name, field_instance.get_default())

    def serialize(self):
        out = {}
        for field_name, field_instance in self.iterfields():
            out[field_name] = field_instance.serialize(getattr(self, field_name))
        return out

    @classmethod
    def deserialize(self, data):
        return self(**data)


class Model(EmbeddedModel):
    @classmethod
    def _get_database_name(self, client):
        return None

    @classmethod
    def _get_database_instance(self, client, database):
        client = client or Client.global_client()
        model_db = self._get_database_name(client)
        if model_db is None:
            database = database or Database.global_database() or client.database()
        else:
            database = client[model_db]
        return database

    @classmethod
    def _get_id_prefix(self):
        return self.__name__

    _id = fields.StrField()
    _rev = fields.StrField()

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
        if not self._id:
            self._id = self._make_id()

    @classmethod
    def _make_id(self):
        return '{:s}.{:016x}.{:s}'.format(
            self._get_id_prefix(),
            int(time.time() * 1000),
            binascii.hexlify(os.urandom(8))
        )

    @classmethod
    def get(self, id, client=None, database=None):
        database = self._get_database_instance(client, database)
        return self.deserialize(database.get(id))

    def save(self, client=None, database=None):
        database = self._get_database_instance(client, database)
        return database.put(self._id, self.serialize())
