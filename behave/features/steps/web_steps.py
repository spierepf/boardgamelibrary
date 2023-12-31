import base64
import json
import pathlib

import requests
from behave import *
from busypie import wait, SECOND
from selenium.webdriver.common.by import By


def find_element_by_id(context, component_id):
    try:
        return context.driver.find_element(By.ID, component_id)
    except:
        return None


def click_element_by_id(context, component_id):
    try:
        context.driver.find_element(By.ID, component_id).click()
        return True
    except:
        return False


def find_element_by_xpath(context, component_xpath):
    try:
        return context.driver.find_element(By.XPATH, component_xpath)
    except:
        return None


def find_autocomplete_list_item_by_text(context, text):
    try:
        for item in context.driver.find_elements(By.CLASS_NAME, "v-list-item__content"):
            if item.text == text:
                return item
    except:
        return None
    return None


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
def step_impl(context, qrcode, component_id):
    component = wait().at_most(10, SECOND).until(
        lambda: find_element_by_xpath(context, f"//div[@id='{component_id}']//input[@type='file']"))
    component.send_keys(str((pathlib.Path(__file__).parent.parent.parent / 'resources' / 'qrcodes' / qrcode).resolve()))


@when(u'we click on the component with id "{component_id}"')
def step_impl(context, component_id):
    component = wait().at_most(10, SECOND).until(lambda: click_element_by_id(context, component_id))


@when(u'we enter the value "{value}" into the autocomplete component with id "{component_id}"')
@when(u'we enter the value "{value}" into the text field component with id "{component_id}"')
def step_impl(context, value, component_id):
    component = wait().at_most(10, SECOND).until(lambda: find_element_by_id(context, component_id))
    component.send_keys(value)


@when(u'we click on the "{option}" option in the autocomplete component with id "{component_id}"')
def step_impl(context, option, component_id):
    component = wait().at_most(10, SECOND).until(lambda: find_autocomplete_list_item_by_text(context, option))
    component.click()


@then('we will see a component with id "{component_id}"')
def step_impl(context, component_id):
    wait().at_most(10, SECOND).until(lambda: find_element_by_id(context, component_id))


@then('we will not see a component with id "{component_id}"')
def step_impl(context, component_id):
    wait().at_most(10, SECOND).until(lambda: find_element_by_id(context, component_id) is None)


@then(u'the text-field with id "{component_id}" will contain "{text}"')
@then(u'the text-field with id "{component_id}" will contain ""')
def step_impl(context, component_id, text=""):
    wait().at_most(10, SECOND).until(lambda: find_element_by_id(context, component_id).get_attribute("value") == text)


@then(u'we will see "{text}" in the dropdown list of the autocomplete component with id "{component_id}"')
def step_impl(context, text, component_id):
    wait().at_most(10, SECOND).until(lambda: find_autocomplete_list_item_by_text(context, text))


@then(u'the autocomplete component with id "{component_id}" will contain "{text}"')
def step_impl(context, component_id, text):
    wait().at_most(10, SECOND).until(lambda: find_element_by_xpath(context,
                                                                   f"//*[@id='{component_id}']/..//span[@class='v-autocomplete__selection-text']").text == text)


@then(u'we will not be logged in')
def step_impl(context):
    wait().at_most(10, SECOND).until(
        lambda: context.driver.execute_script(f'return window.sessionStorage.getItem("auth");') is None)


@then(u'we will be logged in as "{username}"')
def step_impl(context, username):
    auth = wait().at_most(10, SECOND).until(
        lambda: context.driver.execute_script(f'return window.sessionStorage.getItem("auth");'))
    access = json.loads(auth)['access']
    user_id = json.loads(base64.b64decode(access.split('.')[1] + "=="))['user_id']
    assert context.users[username]['id'] == user_id
