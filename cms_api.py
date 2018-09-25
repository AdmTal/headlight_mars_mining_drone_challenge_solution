import requests, json, os
from rate_limiter import rate_limit_to_x_calls_per_second

RATE_LIMIT = int(os.environ['RATE_LIMIT'])  # Per Second


class CmsApi:
    """
    A Utility class to make API calls to the CMS Server
    """

    def __init__(self, callsign):
        self.callsign = callsign

    def register(self):
        return self.__make_http_request('register')

    def scan(self):
        return self.__make_http_request('scan')

    def move(self, x, y):
        return self.__make_http_request('move', {
            'x': str(x),
            'y': str(y)
        })

    def claim(self, node_id):
        return self.__make_http_request('claim', {
            'node': node_id,
        })

    def mine(self, node_id):
        return self.__make_http_request('mine', {
            'node': node_id,
        })

    def release(self, node_id):
        return self.__make_http_request('release', {
            'node': node_id,
        })

    @rate_limit_to_x_calls_per_second(RATE_LIMIT)
    def __make_http_request(self, endpoint, data={}):
        # Inject callsign into all requests
        data.update({
            'callsign': self.callsign,
        })

        location = 'http://{host}:{port}/{endpoint}'.format(
            host=os.environ['SERVER_HOST'],
            port=os.environ['SERVER_PORT'],
            endpoint=endpoint
        )
        response = requests.post(location, data=json.dumps(data))
        return response.json()
