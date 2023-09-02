from behave import *
from selenium.webdriver.common.by import By


@when('we direct the browser to "{url}"')
def step_impl(context, url):
    context.driver.get(f"http://localhost:3000{url}")


@then('we will see a component with id "{id}"')
def step_impl(context, id):
    assert context.driver.find_element(By.ID, id), f"Could not find element with id '{id}'"
