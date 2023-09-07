import os
import pathlib
import subprocess

import requests
from busypie import wait, SECOND

from .behave_layer import BehaveLayer


class ServerLayer(BehaveLayer):
    def before_all(self, context):
        env = os.environ.copy()
        env['BGG_BASE_URL'] = context.bgg_proxy.root()
        context.server_subprocess = subprocess.Popen(
            ["python", "manage.py", "runserver"],
            cwd=pathlib.Path(__file__).parent.parent.parent.resolve(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env
        )

        def verify_server_is_up():
            try:
                requests.get("http://localhost:8000/")
                return True
            except:
                return False

        wait().at_most(10, SECOND).until(verify_server_is_up)

    def after_all(self, context):
        context.server_subprocess.terminate()
