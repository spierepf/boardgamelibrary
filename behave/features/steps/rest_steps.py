import json

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

        response = context.rest_client.post('/testOnly/createUser/',
                                     json={'username': row['username'], 'password': row['password'], 'groups': groups})
        assert response.status_code == 200
        json = response.json()
        assert json['username'] == row['username']
        assert json['groups'] == groups
        context.users[row['username']] = json
        context.passwords[row['username']] = row['password']


@given(u'we have created a title with name "{name}" and bgg_id {bgg_id}')
def step_impl(context, name, bgg_id=None):
    json_body = {'name': name}
    if bgg_id is not None:
        json_body['bgg_id'] = int(bgg_id)
    response = context.rest_client.post(f'/api/library/titles/', json=json_body)
    assert response.status_code == 201, response.text


@when('we perform a GET request on "{path}"')
def step_impl(context, path):
    context.response = context.rest_client.get(path)


@when(u'we perform a POST request on "{path}" with json body \'{json_body}\'')
def step_impl(context, path, json_body):
    context.response = context.rest_client.post(path, json=json.loads(json_body))


@then(u'we get a {status_code} response')
def step_impl(context, status_code):
    assert int(context.response.status_code) == int(status_code), f"Expected {status_code}, got {context.response.status_code}"


@given(u'we have authenticated as "{username}" with password "{password}"')
@when(u'we authenticate as "{username}" with password "{password}"')
def step_impl(context, username, password):
    context.rest_client.authenticate(username, password)


@given(u'we have not authenticated')
def step_impl(context):
    context.rest_client.deauthenticate()


@then(u'we will have an access token')
def step_impl(context):
    assert context.rest_client.has_token()


@then(u'we will not have an access token')
def step_impl(context):
    assert not context.rest_client.has_token()


@then(u'the response body will have a "{key}" entry')
def step_impl(context, key):
    assert key in context.response.json().keys()


@then(u'the result of "{jsonpath}" will be "{value}"')
def step_impl(context, jsonpath, value):
    result = parse(jsonpath).find(context.response.json())
    assert len(result) == 1 and str(result[0].value) == str(value), \
        f"Applying jsonpath {jsonpath} to:\n{context.response.json()}\nExpected: '{value}'\nGot:      '{result[0].value}'"
