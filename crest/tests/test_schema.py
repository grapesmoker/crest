import unittest
import jsonschema


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
        self.assertTrue(result)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            result = self.test_schema.validate(bad_object)

    def test_recursive_traverse(self):

        outer_schema = JSONSchema({
            'title': 'outer_schema',
            'type': 'object',
            'properties': {
                'innerSchema': self.test_schema
            }
        })

        expected = {
            'title': 'outer_schema',
            'type': 'object',
            'properties': {
                'innerSchema': {
                    'title': 'test_schema',
                    'type': 'object',
                    'properties': {
                        'is_good': {
                            'type': 'boolean'
                        },
                        'name': {
                            'type': 'string'
                        },
                        'value': {
                            'type': 'number'
                        }
                    },
                }
            },
        }

        self.assertEqual(outer_schema.schema, expected)

    def test_adjust_paths(self):

        inner_schema = JSONSchema({
            'title': 'inner_schema',
            'type': 'object',
            'properties': {
                'point': {
                    'type': 'object',
                    '$ref': '#/definitions/point'
                }
            },
            'definitions': {
                'point': {
                    'type': 'object',
                    'properties': {
                        'x': {
                            'type': 'number'
                        },
                        'y': {
                            'type': 'number'
                        }
                    }
                }
            }
        }, recompute_refs=False)

        outer_schema = JSONSchema({
            'title': 'outer_schema',
            'type': 'object',
            'properties': {
                'inner_schema': {
                    'type': 'object',
                    '$ref': '#/definitions/inner_schema'
                }
            },
            'definitions': {
                'inner_schema': inner_schema
            }
        }, recompute_refs=False)

        test_element = {
            'inner_schema': {
                'point': {
                    'x': 5,
                    'y': 10
                }
            }
        }
        # before we recompute the definition locations we shouldn't
        # be able to validate this element because we can't find
        # the proper definitions
        with self.assertRaises(jsonschema.exceptions.RefResolutionError):
            result = outer_schema.validate(test_element)

        # now let's recompute the def locations
        outer_schema.adjust_references()
        result = outer_schema.validate(test_element)

        # presto
        self.assertTrue(result)