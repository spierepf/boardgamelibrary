from behave import *
from busypie import SECOND
from selenium.webdriver.common.by import By

from util.wait_at_most import wait_at_most


def find_autocomplete_list_item_by_text(context, text):
    return next(i for i in context.driver.find_elements(By.CLASS_NAME, "v-list-item__content") if i.text == text)


def get_autocomplete_text(context, component_id):
    element = context.driver.find_element(By.ID, component_id)
    parent = element.find_element(By.XPATH, "./..")
    parent_text = parent.text
    element_value = element.get_attribute('value')
    return parent_text + element_value


@when(u'we click on the "{option}" option in the autocomplete component with id "{component_id}"')
@wait_at_most(2, SECOND)
def step_impl(context, option, component_id):
    find_autocomplete_list_item_by_text(context, option).click()


@then(u'the autocomplete component with id "{component_id}" will have an item "{option}"')
@wait_at_most(2, SECOND)
def step_impl(context, component_id, option):
    assert find_autocomplete_list_item_by_text(context, option) is not None


@then(u'the autocomplete component with id "{component_id}" will contain "{text}"')
@then(u'the autocomplete component with id "{component_id}" will contain ""')
@wait_at_most(2, SECOND)
def step_impl(context, component_id, text=""):
    assert get_autocomplete_text(context, component_id) == text
