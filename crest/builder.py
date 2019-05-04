import re

from marshmallow import Schema
from typing import List


class RESTCall(object):

    def __init__(self, methods: List[str], endpoint: str, result_schema: Schema=None,
                 request_schema: Schema=None, api_base: str=''):

        self.methods = methods
        self.api_base = api_base
        self.endpoint = endpoint
        self.result_schema = result_schema
        self.request_schema = request_schema

    @property
    def parent(self):
        if hasattr(self, '_parent'):
            return self._parent
        else:
            return None

    def get(self, **kwargs):
        if hasattr(self, '_GET'):
            return self._GET(**kwargs)
        else:
            raise NotImplementedError('GET not implemented.')

    def put(self, **kwargs):
        if hasattr(self, '_PUT'):
            return self._PUT(**kwargs)
        else:
            raise NotImplementedError('PUT not implemented.')

    def post(self, **kwargs):
        if hasattr(self, '_POST'):
            return self._POST(**kwargs)
        else:
            raise NotImplementedError('POST not implemented.')

    def delete(self, **kwargs):
        if hasattr(self, '_DELETE'):
            return self._DELETE(**kwargs)
        else:
            raise NotImplementedError('DELETE not implemented.')

    def patch(self, **kwargs):
        if hasattr(self, '_PATCH'):
            return self._PATCH(**kwargs)
        else:
            raise NotImplementedError('PATCH not implemented.')

    def connect(self, **kwargs):
        if hasattr(self, '_CONNECT'):
            return self._CONNECT(**kwargs)
        else:
            raise NotImplementedError('CONNECT not implemented.')

    def options(self, **kwargs):
        if hasattr(self, '_OPTIONS'):
            return self._OPTIONS(**kwargs)
        else:
            raise NotImplementedError('OPTIONS not implemented.')

    def trace(self, **kwargs):
        if hasattr(self, '_TRACE'):
            return self._TRACE(**kwargs)
        else:
            raise NotImplementedError('TRACE not implemented.')

    def head(self, **kwargs):
        if hasattr(self, '_HEAD'):
            return self._HEAD(**kwargs)
        else:
            raise NotImplementedError('HEAD not implemented.')

class Get(RESTCall):

    def __init__(self, endpoint, result_schema=None, request_schema=None, api_base=''):
        super(Get, self).__init__(['GET'], endpoint,
                                  result_schema=result_schema,
                                  request_schema=request_schema,
                                  api_base=api_base)


class Post(RESTCall):

    def __init__(self, endpoint, result_schema=None, request_schema=None, api_base=''):
        super(Post, self).__init__(['POST'], endpoint,
                                   result_schema=result_schema,
                                   request_schema=request_schema,
                                   api_base=api_base)


class Put(RESTCall):

    def __init__(self, endpoint, result_schema=None, request_schema=None, api_base=''):
        super(Put, self).__init__(['PUT'], endpoint,
                                  result_schema=result_schema,
                                  request_schema=request_schema,
                                  api_base=api_base)


class Delete(RESTCall):

    def __init__(self, endpoint, result_schema=None, request_schema=None, api_base=''):
        super(Delete, self).__init__(['DELETE'], endpoint,
                                     result_schema=result_schema,
                                     request_schema=request_schema,
                                     api_base=api_base)


class GetPost(RESTCall):

    def __init__(self, endpoint, result_schema=None, request_schema=None, api_base=''):
        super(GetPost, self).__init__(['GET', 'POST'], endpoint,
                                      result_schema=result_schema,
                                      request_schema=request_schema,
                                      api_base=api_base)


class RESTBuilder(type):

    def __new__(mcs, name, bases, namespace):

        rest_class = super().__new__(mcs, name, bases, namespace)

        global_api_base = namespace.get('api_base', None)

        for key, value in namespace.items():
            if isinstance(value, RESTCall):
                for method in value.methods:
                    api_func = mcs.make_method_function(global_api_base, value, method)
                    setattr(value, '_{}'.format(method.upper()), api_func.__get__(value))

        return rest_class

    @classmethod
    def make_method_function(mcs, global_api_base, obj, method):

        def api_func(api_call_obj, **kwargs):
            if api_call_obj.api_base == '' and global_api_base:
                api_base = global_api_base
            elif api_call_obj.api_base != '':
                api_base = api_call_obj.api_base
            else:
                api_base = ''
            url = '{}/{}'.format(api_base, obj.endpoint)
            return api_call_obj.parent.client.invoke(url, method, result_schema=api_call_obj.result_schema, **kwargs)

        return api_func


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

        # inject ourselves into the APICall objects so that they know
        # about the client
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, RESTCall):
                setattr(v, '_parent', self)
