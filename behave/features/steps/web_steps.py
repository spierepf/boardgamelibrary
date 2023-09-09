import base64
import functools
import json
import pathlib

import requests
from behave import *
from busypie import wait, SECOND
from selenium.webdriver.common.by import By


def find_autocomplete_list_item_by_text(context, text):
    return next(i for i in context.driver.find_elements(By.CLASS_NAME, "v-list-item__content") if i.text == text)


def wait_at_most(duration, unit):
    def decorator_wait_at_most(func):
        @functools.wraps(func)
        def wrapper_wait_at_most(*args, **kwargs):
            def wrapper():
                try:
                    func(*args, **kwargs)
                    return True
                except:
                    return False
            wait().at_most(duration, unit).until(wrapper)
        return wrapper_wait_at_most
    return decorator_wait_at_most


@given(u'we are logged in as "{username}"')
def step_impl(context, username):
    context.driver.get(f"http://localhost:3000/")
    response = requests.post('http://localhost:8000/api/token/',
                             data={'username': username, 'password': context.passwords[username]})
    assert response.status_code == 200
    context.driver.execute_script(f"window.sessionStorage.setItem('auth', '{response.text}');")


@given(u'we are not logged in')
def step_impl(context):
    context.driver.get(f"http://localhost:3000/")
    context.driver.execute_script(f'window.sessionStorage.removeItem("auth");')


@when('we direct the browser to "{url}"')
def step_impl(context, url):
    context.driver.get(f"http://localhost:3000{url}")


@when(u'we scan the qrcode "{qrcode}" into the qrcode reader component with id "{component_id}"')
@wait_at_most(2, SECOND)
def step_impl(context, qrcode, component_id):
    context.driver.find_element(By.XPATH, f"//div[@id='{component_id}']//input[@type='file']") \
        .send_keys(str((pathlib.Path(__file__).parent.parent.parent / 'resources' / 'qrcodes' / qrcode).resolve()))


@when(u'we click on the component with id "{component_id}"')
@wait_at_most(2, SECOND)
def step_impl(context, component_id):
    context.driver.find_element(By.ID, component_id).click()


@when(u'we enter the value "{value}" into the autocomplete component with id "{component_id}"')
@when(u'we enter the value "{value}" into the text field component with id "{component_id}"')
@wait_at_most(2, SECOND)
def step_impl(context, value, component_id):
    context.driver.find_element(By.ID, component_id).send_keys(value)


@when(u'we click on the "{option}" option in the autocomplete component with id "{component_id}"')
@wait_at_most(2, SECOND)
def step_impl(context, option, component_id):
    find_autocomplete_list_item_by_text(context, option).click()


@then('we will see a component with id "{component_id}"')
@wait_at_most(5, SECOND)
def step_impl(context, component_id):
    assert context.driver.find_elements(By.ID, component_id)


@then('we will not see a component with id "{component_id}"')
@wait_at_most(2, SECOND)
def step_impl(context, component_id):
    assert not context.driver.find_elements(By.ID, component_id)


@then(u'the text-field with id "{component_id}" will contain "{text}"')
@then(u'the text-field with id "{component_id}" will contain ""')
@wait_at_most(10, SECOND)
def step_impl(context, component_id, text=""):
    assert context.driver.find_element(By.ID, component_id).get_attribute("value") == text


@then(u'we will see "{text}" in the dropdown list of the autocomplete component with id "{component_id}"')
@wait_at_most(2, SECOND)
def step_impl(context, text, component_id):
    assert find_autocomplete_list_item_by_text(context, text) is not None


@then(u'the autocomplete component with id "{component_id}" will contain "{text}"')
@wait_at_most(2, SECOND)
def step_impl(context, component_id, text):
    assert context.driver.find_element(By.XPATH,
                                       f"//*[@id='{component_id}']/..//span[@class='v-autocomplete__selection-text']").text == text


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
