import re
import inspect
from typing import List


class APICallBuilder(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        api_base = kwargs.get('api_base')
        endpoint = kwargs.get('endpoint')
        methods = kwargs.get('methods')
        result_schema = kwargs.get('result_schema')

        api_class = super().__new__(mcs, name, bases, namespace)

        for method in methods:

            expected_kwargs = mcs.parse_endpoint(endpoint)

            def api_func(obj, client, **kwargs):
                print(expected_kwargs)
                url = '{}/{}'.format(api_base, endpoint)
                client.invoke(url, method, result_schema, kwargs)

            setattr(api_class, method.lower(), api_func)

        return api_class

    @classmethod
    def parse_endpoint(cls, endpoint: str):
        """ Parameters to the endpoint e.g. /users/{id} must be in curly braces"""
        param_regex = re.compile(r'\{(.*?)\}')
        params = param_regex.search(endpoint)
        if params:
            expected_kwargs = param_regex.findall(endpoint)
        else:
            expected_kwargs = []
        return expected_kwargs


class APICall(object):

    def __init__(self, methods: List[str], endpoint: str, result_schema, api_base: str=''):

        self.methods = methods
        self.api_base = api_base
        self.endpoint = endpoint
        self.result_schema = result_schema

    @property
    def parent(self):
        if hasattr(self, '_parent'):
            return self._parent
        else:
            return None


class Get(APICall):

    def __init__(self, endpoint, result_schema, api_base=''):
        super(Get, self).__init__(['GET'], endpoint, result_schema, api_base=api_base)


class Post(APICall):

    def __init__(self, endpoint, result_schema, api_base=''):
        super(Post, self).__init__(['POST'], endpoint, result_schema, api_base=api_base)


class RESTBuilder(type):

    def __new__(mcs, name, bases, namespace):

        rest_class = super().__new__(mcs, name, bases, namespace)
        print(namespace)

        def get_self(obj):
            return(obj)
        setattr(rest_class, 'get_self', get_self.__get__(rest_class))

        for key, value in namespace.items():
            if isinstance(value, APICall):
                for method in value.methods:
                    def api_func(obj, **kwargs):
                        url = '{}/{}'.format(value.api_base, value.endpoint)
                        return obj.parent.client.invoke(url, method, value.result_schema, **kwargs)

                    setattr(value, method.lower(), api_func.__get__(value))
                    print(value.__dict__)

        return rest_class

    @classmethod
    def parse_endpoint(mcs, endpoint: str):
        """ Parameters to the endpoint e.g. /users/{id} must be in curly braces"""
        param_regex = re.compile(r'\{(.*?)\}')
        params = param_regex.search(endpoint)
        if params:
            expected_kwargs = param_regex.findall(endpoint)
        else:
            expected_kwargs = []
        return expected_kwargs


class RESTInterface(metaclass=RESTBuilder):

    def __init__(self, client):

        self.client = client

        for k, v in self.__class__.__dict__.items():
            if isinstance(v, APICall):
                setattr(v, '_parent', self)

    def get_self(self):
        return self


# class Foo(RESTInterface):
#
#     foo = Get('users', None, 'api')




# want to be able to write:

# class Foo(object):
#
#     access = APICall('access', 'GET', 'access', AccessSchema)
#     config = APICall('access', 'GET', 'access/config', AccessConfigSchema)
#
# f = Foo()
# f.access(client)