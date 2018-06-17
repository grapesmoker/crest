import requests


class Client(object):

    def __init__(self, host, port=80):

        self.host = host
        self.port = port
        if port != 80:
            self.url = '{}:{}'.format(host, port)
        else:
            self.url = host

    def invoke(self, endpoint, method, result_schema, **kwargs):

        params = kwargs.pop('params', None)

        url = (self.url + '/' + endpoint).format(**kwargs)
        if method == 'GET':
            result = requests.get(url, params=params)
            return result.json()