import unittest
import jsonschema

from crest.schema import BaseSchema, JSONSchema


class TestSchema(unittest.TestCase):

    def setUp(self):

        self.schema_dict = {
            'title': 'test_schema',
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string'
                },
                'value': {
                    'type': 'number'
                },
                'is_good': {
                    'type': 'boolean'
                }
            }
        }

        self.test_schema = JSONSchema(self.schema_dict)

    def test_base_exceptions(self):

        bs = BaseSchema({})
        with self.assertRaises(NotImplementedError):
            schema = bs.schema

        with self.assertRaises(NotImplementedError):
            bs.validate({})

    def test_json_schema_validation(self):

        self.assertEqual(self.schema_dict, self.test_schema.schema)
        good_object = {'name': 'jerry', 'value': 10.5, 'is_good': True}
        bad_object = {'name': 'jerry', 'value': True, 'is_good': 10.5}
        result = self.test_schema.validate(good_object)
        self.assertIsNone(result)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            result = self.test_schema.validate(bad_object)

