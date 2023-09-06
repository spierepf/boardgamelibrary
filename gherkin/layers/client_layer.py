import pathlib
import subprocess

import requests
from busypie import wait, SECOND

from .behave_layer import BehaveLayer


class ClientLayer(BehaveLayer):
    def before_all(self, context):
        context.client_subprocess = subprocess.Popen(
            ["yarn", "dev"],
            cwd=(pathlib.Path(__file__).parent.parent.parent / "client").resolve(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        def verify_client_is_up():
            try:
                requests.get("http://localhost:3000/")
                return True
            except:
                return False

        wait().at_most(10, SECOND).until(verify_client_is_up)

    def after_all(self, context):
        context.client_subprocess.terminate()
