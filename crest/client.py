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

        if request_schema is not None:
            request_schema.validate(params)

        url = (self.url + '/' + endpoint).format(**kwargs)
        if method == 'GET':
            if self.token:
                self.headers['Authorization'] = self.token
                result = requests.get(url, params=params, headers=self.headers)
            elif self.auth:
                result = requests.get(url, auth=self.auth, params=params, headers=self.headers)
            else:
                result = requests.get(url, params=params, headers=self.headers)

            if result_schema:
                result_schema.validate(result.json())
            return result.json()

        elif method == 'POST':
            self.headers['Content-Type'] = 'application/json'
            if self.token:
                self.headers['Authorization'] = self.token
                result = requests.post(url, json=params, headers=self.headers)
            elif self.auth:
                result = requests.post(url, auth=self.auth, json=params, headers=self.headers)
            else:
                result = requests.post(url, json=params, headers=self.headers)

            if result_schema:
                result_schema.validate(result.json())
            return result.json()