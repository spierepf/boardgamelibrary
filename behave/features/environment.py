import pathlib
import subprocess

import requests
from busypie import wait, SECOND
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_all(context):
    context.server_subprocess = subprocess.Popen(
        ["python manage.py runserver"],
        cwd=pathlib.Path(__file__).parent.parent.parent.resolve(),
        shell=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    def verify_server_is_up():
        try:
            requests.get("http://localhost:8000/")
            return True
        except:
            return False

    wait().at_most(10, SECOND).until(verify_server_is_up)

    context.client_subprocess = subprocess.Popen(
        ["yarn dev"],
        cwd=(pathlib.Path(__file__).parent.parent.parent / "client").resolve(),
        shell=True,
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

    options = Options()
    options.headless = True
    context.driver = webdriver.Chrome(options)


def after_all(context):
    context.server_subprocess.kill()
    context.client_subprocess.kill()
