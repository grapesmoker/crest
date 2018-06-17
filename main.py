from pprint import pprint

from crest.builder import Get, RESTInterface
from crest.client import Client

if __name__ == '__main__':

    class TestREST(RESTInterface):

        user = Get('users/{id}', None, 'api')
        users = Get('users', None, 'api')

    client = Client('http://reqres.in')

    test = TestREST(client)
    result = test.users.get()
    pprint(result)
    result = test.user.get(id=2)
    pprint(result)