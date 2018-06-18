from pprint import pprint

from crest.builder import Get, RESTInterface
from crest.client import Client
from crest.schema import JSONSchema


result_schema = {
    'title': 'reqres_test_schema',
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'avatar': {
                    'type': 'string'
                },
                'first_name': {
                    'type': 'string'
                },
                'last_name': {
                    'type': 'string'
                },
                'id': {
                    'type': 'integer'
                }
            }
        }
    }
}

if __name__ == '__main__':

    class TestREST(RESTInterface):

        api_base = 'api'
        user = Get('users/{id}', JSONSchema(result_schema))
        users = Get('users', None)

    client = Client('http://reqres.in')

    test = TestREST(client)
    result = test.users.get()
    pprint(result)
    result = test.user.get(id=2)
    pprint(result)