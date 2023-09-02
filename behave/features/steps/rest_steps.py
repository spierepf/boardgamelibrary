import requests
from behave import *


@when('we perform a GET request on "{url}"')
def step_impl(context, url):
    context.response = requests.get(f'http://localhost:8000{url}')


@then(u'we get a {status_code} response')
def step_impl(context, status_code):
    assert int(context.response.status_code) == int(
        status_code), f"Expected {status_code}, got {context.response.status_code}"
