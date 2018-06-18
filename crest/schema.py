import jsonschema

from abc import abstractmethod


class BaseSchema(object):

    @property
    @abstractmethod
    def schema(self):
        raise NotImplementedError

    def __init__(self, schema):

        self._schema = schema

    @abstractmethod
    def validate(self, obj):
        raise NotImplementedError


class JSONSchema(BaseSchema):

    @property
    def schema(self):
        return self._schema

    def validate(self, obj):
        jsonschema.validate(obj, self._schema)
        return True

