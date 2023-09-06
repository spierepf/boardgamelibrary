import requests

from .behave_layer import BehaveLayer


class ResetLayer(BehaveLayer):
    def before_scenario(self, context, scenario):
        response = requests.get("http://localhost:8000/testOnly/reset/")
        assert response.status_code == 200
        context.token = None
        context.users = {}
        context.passwords = {}
