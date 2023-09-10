import requests

from util.rest_client import RestClient
from .behave_layer import BehaveLayer


class ResetLayer(BehaveLayer):
    def before_scenario(self, context, scenario):
        response = requests.get("http://localhost:8000/testOnly/reset/")
        assert response.status_code == 200
        context.rest_client = RestClient()
        context.users = {}
        context.passwords = {}
