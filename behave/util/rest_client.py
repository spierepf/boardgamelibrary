import requests


class RestClient:
    AUTH_HEADER = 'authorization'

    def __init__(self, token=None):
        self._token = token

    def headers(self):
        headers = {}
        if self._token:
            headers[RestClient.AUTH_HEADER] = f"Bearer {self._token}"
        return headers

    def post(self, path, json):
        return requests.post(f'http://localhost:8000{path}', headers=self.headers(), json=json)

    def get(self, path):
        url = path if path.startswith('http') else f'http://localhost:8000{path}'
        return requests.get(url, headers=self.headers())

    def deauthenticate(self):
        self._token = None

    def authenticate(self, username, password):
        self.deauthenticate()
        response = self.post('/api/token/', {'username': username, 'password': password})
        if response.status_code == 200:
            self._token = response.json()['access']

    def has_token(self):
        return self._token is not None
