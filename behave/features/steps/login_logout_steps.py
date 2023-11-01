import base64
import json

import requests
from behave import *
from busypie import SECOND

from util.wait_at_most import wait_at_most


@given(u'we are logged in as "{username}"')
def step_impl(context, username):
    context.driver.get(f"http://localhost:3000/")
    response = requests.post('http://localhost:8000/api/token/', data={'username': username, 'password': context.passwords[username]})
    assert response.status_code == 200
    context.driver.execute_script(f"window.sessionStorage.setItem('auth', '{response.text}');")


@given(u'we are not logged in')
def step_impl(context):
    context.driver.get(f"http://localhost:3000/")
    context.driver.execute_script(f'window.sessionStorage.removeItem("auth");')


@then(u'we will not be logged in')
@wait_at_most(2, SECOND)
def step_impl(context):
    assert context.driver.execute_script(f'return window.sessionStorage.getItem("auth");') is None


@then(u'we will be logged in as "{username}"')
@wait_at_most(2, SECOND)
def step_impl(context, username):
    auth = context.driver.execute_script(f'return window.sessionStorage.getItem("auth");')
    access = json.loads(auth)['access']
    user_id = json.loads(base64.b64decode(access.split('.')[1] + "=="))['user_id']
    assert context.users[username]['id'] == user_id
