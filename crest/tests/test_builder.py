import unittest
import marshmallow

from marshmallow import Schema, fields
from crest.builder import RESTInterface, RESTBuilder, Get, Post, Delete, Put, GetPost
from crest.client import Client


class TestBuilder(unittest.TestCase):

    def setUp(self):

        class TestREST(RESTInterface):
            api_base = 'api'

            users = Get('users')
            post_user = Post('users/{id}')
            user = GetPost('users/{id}')
            delete_user = Delete('users/{id}')
            put_user = Put('users/{id}')

        self.client = Client('https://reqres.in')
        self.test_rest = TestREST(self.client)

    def test_parse_endpoint(self):

        url = 'users/{user_id}/posts/{post_id}'
        expected_args = ['user_id', 'post_id']
        args = RESTBuilder.parse_endpoint(url)
        self.assertEqual(expected_args, args)

        other_url = 'users/posts/stuff'
        args = RESTBuilder.parse_endpoint(other_url)
        self.assertEqual(args, [])

    def test_make_method_functions(self):

        func1 = RESTBuilder.make_method_function('api', self.test_rest.user, 'GET')
        func2 = RESTBuilder.make_method_function('api', self.test_rest.user, 'POST')

        self.assertIsNot(func1, func2)

    def test_class_members_have_method_functions(self):

        self.assertIsNotNone(getattr(self.test_rest.users, 'get'))
        self.assertIsNotNone(getattr(self.test_rest.user, 'get'))
        self.assertIsNotNone(getattr(self.test_rest.user, 'post'))
        self.assertIsNotNone(getattr(self.test_rest.post_user, 'post'))
        self.assertIsNotNone(getattr(self.test_rest.put_user, 'put'))
        self.assertIsNotNone(getattr(self.test_rest.delete_user, 'delete'))

    def test_class_members_have_parent(self):

        self.assertIs(self.test_rest.user.parent, self.test_rest)
        self.assertIs(self.test_rest.users.parent, self.test_rest)

    def test_get_users(self):

        expected = {
            "page": 1,
            "per_page": 3,
            "total": 12,
            "total_pages": 4,
            "data": [{
                "id": 1,
                "first_name": "George",
                "last_name": "Bluth",
                "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/calebogden/128.jpg"
            }, {
                "id": 2,
                "first_name": "Janet",
                "last_name": "Weaver",
                "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/josephstein/128.jpg"
            }, {
                "id": 3,
                "first_name": "Emma",
                "last_name": "Wong",
                "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/olegpogodaev/128.jpg"
            }]
        }

        result = self.test_rest.users.get()
        self.assertEqual(result, expected)

        expected = {
            "data": {
                "id": 2,
                "first_name": "Janet",
                "last_name": "Weaver",
                "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/josephstein/128.jpg"
            }
        }

        result = self.test_rest.user.get(id=2)
        self.assertEqual(result, expected)

    def test_without_global_api_base(self):

        class TestREST(RESTInterface):

            users = Get('users', api_base='api')
            user = GetPost('users/{id}', api_base='api')

        test_rest = TestREST(self.client)

        expected = {
            "page": 1,
            "per_page": 3,
            "total": 12,
            "total_pages": 4,
            "data": [{
                "id": 1,
                "first_name": "George",
                "last_name": "Bluth",
                "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/calebogden/128.jpg"
            }, {
                "id": 2,
                "first_name": "Janet",
                "last_name": "Weaver",
                "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/josephstein/128.jpg"
            }, {
                "id": 3,
                "first_name": "Emma",
                "last_name": "Wong",
                "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/olegpogodaev/128.jpg"
            }]
        }

        result = test_rest.users.get()
        self.assertEqual(result, expected)

        expected = {
            "data": {
                "id": 2,
                "first_name": "Janet",
                "last_name": "Weaver",
                "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/josephstein/128.jpg"
            }
        }

        result = test_rest.user.get(id=2)
        self.assertEqual(result, expected)

    def test_with_schema_validation(self):

        class GoodUserSchema(Schema):
            id = fields.Integer()
            first_name = fields.String()
            last_name = fields.String()
            avatar = fields.URL()

        class BadUserSchema(Schema):
            id = fields.Integer()
            first_name = fields.String()
            last_name = fields.String()
            avatar = fields.Number()

        class GoodDataSchema(Schema):
            data = fields.Nested(GoodUserSchema)

        class BadDataSchema(Schema):
            data = fields.Nested(BadUserSchema)

        result_schema = GoodDataSchema()

        class TestREST(RESTInterface):
            user = GetPost('users/{id}', api_base='api', result_schema=result_schema)

        test_rest = TestREST(self.client)
        result = test_rest.user.get(id=2)
        self.assertIsNotNone(result)

        result_schema = BadDataSchema()

        with self.assertRaises(marshmallow.exceptions.ValidationError):
            result = self.client.invoke('api/users/{id}', 'GET', result_schema=result_schema, id=2)

    def test_not_implemented(self):

        class TestREST(RESTInterface):
            user = GetPost('users/{id}', api_base='api')

        test_rest = TestREST(self.client)

        with self.assertRaises(NotImplementedError):
            test_rest.user.delete(id=2)

# TODO: write some tests for validating on the request schema
# TODO: refactor tests