import time
import os
import binascii

import fields


class EmbeddedModel(object):
    @classmethod
    def iterfields(self):
        # TODO: cache this
        for field_name, field_instance in vars(self).items():
            if isinstance(field_instance, fields.Field):
                yield field_name, field_instance

    def __init__(self, **kwargs):
        # TODO: cache this
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
    __database__ = lambda cls, db: db.database()
    __id_prefix__ = lambda cls: cls.__name__

    _id = fields.StrField()
    _rev = fields.StrField()

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
        if not self._id:
            self._id = self._make_id()

    @classmethod
    def _make_id(self):
        prefix = None
        if callable(self.__id_prefix__):
            prefix = self.__id_prefix__(self)
        elif self.__id_prefix__:
            prefix = self.__id_prefix__
        else:
            prefix = self.__name__

        return '{:s}.{:016x}.{:s}'.format(
            prefix,
            int(time.time() * 1000),
            binascii.hexlify(os.urandom(8))
        )
