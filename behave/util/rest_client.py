import requests


class RestClient:
    AUTH_HEADER = 'authorization'

    def __init__(self, token=None):
        self.token = token

    def headers(self):
        headers = {}
        if self.token:
            headers[RestClient.AUTH_HEADER] = f"Bearer {self.token}"
        return headers

    def post(self, path, json):
        return requests.post(f'http://localhost:8000{path}', headers=self.headers(), json=json)

    def get(self, path):
        return requests.get(f'http://localhost:8000{path}', headers=self.headers())
