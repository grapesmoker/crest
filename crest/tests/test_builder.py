import unittest

from crest.builder import RESTInterface, Get, Post, GetPost
from crest.client import Client


class TestBuilder(unittest.TestCase):

    def setUp(self):

        class TestREST(RESTInterface):

            api_base = 'api'

            users = Get('users')
            user = GetPost('users/{id}')

        self.client = Client('https://reqres.in')
        self.test_rest = TestREST(self.client)

    def test_class_members_have_method_functions(self):

        self.assertIsNotNone(getattr(self.test_rest.users, 'get'))
        self.assertIsNotNone(getattr(self.test_rest.user, 'get'))
        self.assertIsNotNone(getattr(self.test_rest.user, 'post'))

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