import unittest

from crest.client import Client


class TestClient(unittest.TestCase):

    def setUp(self):

        self.client = Client('https://reqres.in')

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
        result = self.client.invoke('api/users', 'GET')
        self.assertEqual(result, expected)

    def test_get_users_with_params(self):

        expected = {
            "page": 2,
            "per_page": 3,
            "total": 12,
            "total_pages": 4,
            "data": [
                {
                    "id": 4,
                    "first_name": "Eve",
                    "last_name": "Holt",
                    "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/marcoramires/128.jpg"
                },
                {
                    "id": 5,
                    "first_name": "Charles",
                    "last_name": "Morris",
                    "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/stephenmoon/128.jpg"
                },
                {
                    "id": 6,
                    "first_name": "Tracey",
                    "last_name": "Ramos",
                    "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/bigmancho/128.jpg"
                }
            ]
        }

        result = self.client.invoke('api/users', 'GET', params={'page': 2})
        self.assertEqual(result, expected)

    def test_get_single_user(self):

        expected = {
            "data": {
                "id": 2,
                "first_name": "Janet",
                "last_name": "Weaver",
                "avatar": "https://s3.amazonaws.com/uifaces/faces/twitter/josephstein/128.jpg"
            }
        }

        result = self.client.invoke('api/users/{id}', 'GET', id=2)
        self.assertEqual(result, expected)

    def test_post_user(self):

        data = {'name': 'morpheus', 'job': 'leader'}
        result = self.client.invoke('api/users', 'POST', params=data)
        self.assertEqual(result['name'], 'morpheus')
        self.assertEqual(result['job'], 'leader')
        self.assertIn('id', result)
        self.assertIn('createdAt', result)

    def test_register(self):

        data = {'email': 'joe@schmoe.com', 'password': 'password'}
        result = self.client.invoke('api/register', 'POST', params=data)
        self.assertIn('token', result)
        token = result['token']
        print(token)

    def test_auth_user(self):

        pass
