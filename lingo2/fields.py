# import inspect
from datetime import datetime

from dateutil.parser import parse
import pytz


class Field(object):
    def __init__(self, default=None, validators=None, doc=None, type_=None, **kwargs):
        self.type_ = type_ or str
        self.default = default
        self.validators = validators or []
        self.doc = doc

    def get_default(self):
        return self.default() if callable(self.default) else self.default

    def serialize(self, value):
        if value is None:
            return None
        return self.type_(value)

    def deserialize(self, value):
        if value is None:
            return None
        return self.type_(value)


class ListField(Field):
    def __init__(self, subtype, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        self.subtype = subtype

    def serialize(self, value):
        if value is None:
            return None
        return map(self.subtype.serialize, value)

    def deserialize(self, value):
        if value is None:
            return None
        if not isinstance(value, list):
            value = [value]
        return map(self.subtype.deserialize, value)


class DictField(Field):
    def __init__(self, subtype, *args, **kwargs):
        super(DictField, self).__init__(*args, **kwargs)
        self.subtype = subtype

    def serialize(self, value):
        if value is None:
            return None
        return {k: self.subtype.serialize(v) for k, v in value.items()}

    def deserialize(self, value):
        if value is None:
            return None
        return {k: self.subtype.deserialize(v) for k, v in value.items()}


class StrField(Field):
    def __init__(self, *args, **kwargs):
        super(StrField, self).__init__(type_=str, *args, **kwargs)


class IntField(Field):
    def __init__(self, *args, **kwargs):
        super(IntField, self).__init__(type_=int, *args, **kwargs)


class FloatField(Field):
    def __init__(self, *args, **kwargs):
        super(FloatField, self).__init__(type_=float, *args, **kwargs)


class UnicodeField(Field):
    def __init__(self, encoding=None, *args, **kwargs):
        super(UnicodeField, self).__init__(*args, **kwargs)
        self.encoding = encoding or 'utf-8'

    def serialize(self, value):
        if not isinstance(value, unicode):
            return value
        return value.encode(self.encoding)

    def deserialize(self, value):
        if isinstance(value, unicode):
            value = str(value)
        return value.decode(self.encoding)


class ModelField(Field):
    def __init__(self, model, *args, **kwargs):
        super(ModelField, self).__init__(*args, **kwargs)
        self.model = model

    def serialize(self, value):
        return value.serialize() if value else None

    def deserialize(self, value):
        return self.model.deserialize(value) if value else None


class DateField(Field):
    def serialize(self, value):
        if value is None:
            return None
        return value.isoformat()

    def deserialize(self, value):
        if value is None:
            return None
        return parse(str(value)).date()


class DateTimeField(Field):
    def _fix_tz(self, value):
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            value = value.replace(tzinfo=pytz.timezone('UTC'))
        return value

    def serialize(self, value):
        if value is None:
            return None
        return self._fix_tz(value).isoformat()

    def deserialize(self, value):
        if value is None:
            return None
        return self._fix_tz(parse(str(value)))
