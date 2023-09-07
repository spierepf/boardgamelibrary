import requests
from behave import *


@given(u'the following users exist')
def step_impl(context):
    for row in context.table:
        if 'groups' in row.headings:
            groups = row['groups'].split(",")
            if groups == [""]:
                groups = []
        else:
            groups = []

        response = requests.post('http://localhost:8000/testOnly/createUser/',
                                 json={'username': row['username'], 'password': row['password'], 'groups': groups})
        assert response.status_code == 200
        json = response.json()
        assert json['username'] == row['username']
        assert json['groups'] == groups
        context.users[row['username']] = json
        context.passwords[row['username']] = row['password']


@when('we perform a GET request on "{url}"')
def step_impl(context, url):
    headers = {}
    if context.token:
        headers['authorization'] = f"Bearer {context.token}"
    context.response = requests.get(f'http://localhost:8000{url}', headers=headers)


@then(u'we get a {status_code} response')
def step_impl(context, status_code):
    assert int(context.response.status_code) == int(
        status_code), f"Expected {status_code}, got {context.response.status_code}"


@given(u'we have authenticated as "{username}" with password "{password}"')
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


@then(u'the response body will have a "{key}" entry')
def step_impl(context, key):
    assert key in context.response.json().keys()
