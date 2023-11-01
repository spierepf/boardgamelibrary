import pathlib

from behave import *
from busypie import SECOND
from selenium.webdriver.common.by import By

from util.wait_at_most import wait_at_most


@when('we direct the browser to "{url}"')
def step_impl(context, url):
    context.driver.get(f"http://localhost:3000{url}")


@when(u'we scan the qrcode "{qrcode}" into the qrcode reader component with id "{component_id}"')
@wait_at_most(2, SECOND)
def step_impl(context, qrcode, component_id):
    context.driver.find_element(By.XPATH, f"//div[@id='{component_id}']//input[@type='file']") \
        .send_keys(str((pathlib.Path(__file__).parent.parent.parent / 'resources' / 'qrcodes' / qrcode).resolve()))


@when(u'we click on the component with id "{component_id}"')
@wait_at_most(5, SECOND)
def step_impl(context, component_id):
    context.driver.find_element(By.ID, component_id).click()


@when(u'we enter the value "{value}" into the component with id "{component_id}"')
@wait_at_most(2, SECOND)
def step_impl(context, value, component_id):
    context.driver.find_element(By.ID, component_id).send_keys(value)


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


@step('the component with id "{component_id}" will include the substring "{substring}"')
@wait_at_most(10, SECOND)
def step_impl(context, component_id, substring=""):
    assert substring in context.driver.find_element(By.ID, component_id).text
