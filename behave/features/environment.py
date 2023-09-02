import os
import pathlib
import signal
import subprocess

import requests
from busypie import wait, SECOND


def before_all(context):
    context.server_subprocess = subprocess.Popen(
        ["python manage.py runserver"],
        cwd=pathlib.Path(__file__).parent.parent.parent.resolve(),
        shell=True,
    )

    def verify_server_is_up():
        try:
            requests.get("http://localhost:8000/")
            return True
        except:
            return False

    wait().at_most(10, SECOND).until(verify_server_is_up)


def after_all(context):
    os.killpg(os.getpgid(context.server_subprocess.pid), signal.SIGTERM)
