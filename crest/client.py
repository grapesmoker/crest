import simplejson
import requests


class Client(object):

    def __init__(self, host, port=80, user=None, password=None, token=None):

        self.host = host
        self.port = port
        if port != 80:
            self.url = '{}:{}'.format(host, port)
        else:
            self.url = host

        self.user = user
        self.password = password
        self.token = token

        self.headers = {}

        self.auth = None

        if user and password:
            self.auth = (user, password)

    def invoke(self, endpoint, method, result_schema=None, request_schema=None, **kwargs):

        params = kwargs.pop('params', None)
        body = kwargs.pop('body', None)

        url = (self.url + '/' + endpoint).format(**kwargs)
        if method == 'GET':
            if self.token:
                self.headers['Authorization'] = self.token
                result = requests.get(url, params=params, headers=self.headers)
            elif self.auth:
                result = requests.get(url, auth=self.auth, params=params, headers=self.headers)
            else:
                result = requests.get(url, params=params, headers=self.headers)

        elif method == 'POST':
            if request_schema is not None:
                request_schema.validate(params)
            self.headers['Content-Type'] = 'application/json'
            if self.token:
                self.headers['Authorization'] = self.token
                result = requests.post(url, json=body, headers=self.headers)
            elif self.auth:
                result = requests.post(url, auth=self.auth, json=body, headers=self.headers)
            else:
                result = requests.post(url, json=body, headers=self.headers)

        elif method == 'PUT':
            if request_schema is not None:
                request_schema.validate(params)
            self.headers['Content-Type'] = 'application/json'
            if self.token:
                self.headers['Authorization'] = self.token
                result = requests.put(url, json=body, headers=self.headers)
            elif self.auth:
                result = requests.put(url, auth=self.auth, json=body, headers=self.headers)
            else:
                result = requests.put(url, json=body, headers=self.headers)

        elif method == 'DELETE':
            self.headers['Content-Type'] = 'application/json'
            if self.token:
                self.headers['Authorization'] = self.token
                result = requests.delete(url, params=params, headers=self.headers)
            elif self.auth:
                result = requests.delete(url, auth=self.auth, params=params, headers=self.headers)
            else:
                result = requests.delete(url, params=params, headers=self.headers)

        try:
            result_json = result.json()
        except simplejson.JSONDecodeError as ex:
            return {
                'code': result.status_code,
                'content': result.content,
                'message': result.reason,
                'error': ex.msg
            }

        if result.status_code in [200, 201, 202] and result_schema:
            result_schema.validate(result_json)
            return result_json
        elif result.status_code in [200, 201, 202] and not result_schema:
            return result_json
        else:
            return {
                'code': result.status_code,
                'response': result_json,
                'message': result.reason
            }