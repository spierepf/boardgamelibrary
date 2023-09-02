import pathlib

from behave import *
from busypie import wait, SECOND
from selenium.webdriver.common.by import By


def find_element_by_id(context, component_id):
    try:
        return context.driver.find_element(By.ID, component_id)
    except:
        return None


def find_element_by_xpath(context, component_xpath):
    try:
        return context.driver.find_element(By.XPATH, component_xpath)
    except:
        return None


@when('we direct the browser to "{url}"')
def step_impl(context, url):
    context.driver.get(f"http://localhost:3000{url}")


@when(u'we scan the qrcode "{qrcode}" into the qrcode reader component with id "{component_id}"')
def step_impl(context, qrcode, component_id):
    component = wait().at_most(10, SECOND).until(
        lambda: find_element_by_xpath(context, f"//div[@id='{component_id}']//input[@type='file']"))
    component.send_keys(str((pathlib.Path(__file__).parent.parent / "qrcodes" / qrcode).resolve()))


@then('we will see a component with id "{component_id}"')
def step_impl(context, component_id):
    wait().at_most(10, SECOND).until(lambda: find_element_by_id(context, component_id))


@then(u'the text-field with id "{component_id}" will contain "{text}"')
@then(u'the text-field with id "{component_id}" will contain ""')
def step_impl(context, component_id, text=""):
    wait().at_most(10, SECOND).until(lambda: find_element_by_id(context, component_id).get_attribute("value") == text)
