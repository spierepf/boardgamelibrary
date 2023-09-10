import json

import requests
from behave import *
from jsonpath_ng import parse


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


@given(u'we have created a title with name "{name}" and bgg_id {bgg_id}')
def step_impl(context, name, bgg_id=None):
    headers = {'Content-type': 'application/json'}
    if context.token:
        headers['authorization'] = f"Bearer {context.token}"
    json_body = {'name': name}
    if bgg_id is not None:
        json_body['bgg_id'] = int(bgg_id)
    response = requests.post(f'http://localhost:8000/api/library/titles/', headers=headers, json=json_body)
    assert response.status_code == 201, response.text


@when('we perform a GET request on "{url}"')
def step_impl(context, url):
    headers = {}
    if context.token:
        headers['authorization'] = f"Bearer {context.token}"
    context.response = requests.get(f'http://localhost:8000{url}', headers=headers)


@when(u'we perform a POST request on "{url}" with json body \'{json_body}\'')
def step_impl(context, url, json_body):
    headers = {'Content-type': 'application/json'}
    if context.token:
        headers['authorization'] = f"Bearer {context.token}"
    context.response = requests.post(f'http://localhost:8000{url}', headers=headers, json=json.loads(json_body))


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


@given(u'we have not authenticated')
def step_impl(context):
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


@then(u'the result of "{jsonpath}" will be "{value}"')
def step_impl(context, jsonpath, value):
    result = parse(jsonpath).find(context.response.json())
    assert len(result) == 1 and str(result[0].value) == str(value),\
        f"Applying jsonpath {jsonpath} to:\n{context.response.json()}\nExpected: '{value}'\nGot:      '{result[0].value}'"
