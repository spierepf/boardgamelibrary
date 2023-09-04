import requests
from behave import *


@given(u'the following users exist')
def step_impl(context):
    for row in context.table:
        response = requests.post('http://localhost:8000/testOnly/createUser/',
                                 json={'username': row['username'], 'password': row['password']})
        assert response.status_code == 200
        assert response.json()['username'] == row['username']


@when('we perform a GET request on "{url}"')
def step_impl(context, url):
    context.response = requests.get(f'http://localhost:8000{url}')


@then(u'we get a {status_code} response')
def step_impl(context, status_code):
    assert int(context.response.status_code) == int(
        status_code), f"Expected {status_code}, got {context.response.status_code}"


@when(u'we authenticate as "{username}" with password "{password}"')
def step_impl(context, username, password):
    response = requests.post('http://localhost:8000/api/token/', data={'username': username, 'password': password})
    if response.status_code == 200:
        context.token = response.json()['access']
    else:
        context.token = None


@then(u'we will have an access token')
def step_impl(context):
    assert context.token is not None


@then(u'we will not have an access token')
def step_impl(context):
    assert context.token is None
