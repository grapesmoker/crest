import copy
import json
import jsonschema
import os
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

    def __init__(self, schema, recompute_refs=True):

        if isinstance(schema, str):
            # maybe this is a string in json?
            try:
                schema = json.loads(schema)
            except json.JSONDecodeError as ex:
                # guess not, fail silently
                # maybe this is a path to a file
                schema = json.load(open(os.path.abspath(schema)))

        super(JSONSchema, self).__init__(schema)
        self.replace_objects()
        if recompute_refs:
            self.adjust_references()

    @property
    def schema(self):
        return self._schema

    def validate(self, obj):
        jsonschema.validate(obj, self._schema)
        return True

    def replace_objects(self):
        """ Recursively traverse the current schema, replacing
            any schema objects found in it with copies of their dicts
        """

        def recursive_traverse(schema, key):
            value = schema[key]
            if isinstance(value, dict):
                for subkey in value:
                    recursive_traverse(value, subkey)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    recursive_traverse(item, index)
            elif isinstance(value, JSONSchema):
                value = schema[key] = copy.deepcopy(value.schema)
                for subkey in value:
                    recursive_traverse(value, subkey)

        for key in self.schema:
            recursive_traverse(self.schema, key)

    def adjust_references(self):
        """ Recursively crawl the tree and relabel all the references that are
            defined internally in subschemas to whatever locations the objects
            are actually defined in. This logic depends on definitions always
            living inside the `definitions` object, so if that's not true,
            ¯\_(ツ)_/¯
        """

        element_references = set()
        defined_objects = set()

        def recursive_adjust(schema, key, path):
            value = schema[key]
            current_path = path + '/' + str(key)
            parent = path.split('/')[-1]
            if parent == 'definitions':
                defined_objects.add(current_path)
            if key == '$ref':
                element = value.split('/')[-1]
                element_references.add((element, current_path))
            if isinstance(value, dict):
                for subkey in value:
                    recursive_adjust(value, subkey, current_path)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    recursive_adjust(item, index, current_path)

        for key in self.schema:
            recursive_adjust(self.schema, key, '#')

        for element, location in element_references:
            new_location = [item for item in defined_objects if item.endswith(element)][0]
            self._set_element_by_path(location.lstrip('#/'), new_location)

    def _set_element_by_path(self, path, value):
        """ Takes a slash-delimited absolute path and sets the thing at that path to the value """
        path = path.split('/')
        current_element = self.schema
        for elem in path[:-1]:
            if elem.isnumeric():
                elem = int(elem)
            current_element = current_element[elem]
        current_element[path[-1]] = value

    def __str__(self):
        return json.dumps(self.schema)

    def __repr__(self):
        return json.dumps(self.schema)