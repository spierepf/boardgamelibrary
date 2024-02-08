import time

from behave import *
from busypie import SECOND
from selenium.webdriver.common.by import By

from util.wait_at_most import wait_at_most


def select_component_xpath(component_id):
    return f"//input[@id='{component_id}']//ancestor::div[@class='v-field__input']"


def select_component_option_xpath(option):
    return f"//div[@class='v-overlay-container']//div[text()='{option}']"


@when(u'we select the "{option}" option in the select component with id "{component_id}"')
@wait_at_most(2, SECOND)
def step_impl(context, option, component_id):
    context.driver.find_element(By.XPATH, select_component_xpath(component_id)).click()
    time.sleep(1)
    context.driver.find_element(By.XPATH, select_component_option_xpath(option)).click()


@then(u'the select component with id "{component_id}" will have an item "{option}"')
@wait_at_most(2, SECOND)
def step_impl(context, component_id, option):
    context.driver.find_element(By.XPATH, select_component_xpath(component_id)).click()
    time.sleep(1)
    assert context.driver.find_elements(By.XPATH, select_component_option_xpath(option))


@then(u'the select component with id "{component_id}" will not have an item "{option}"')
@wait_at_most(2, SECOND)
def step_impl(context, component_id, option):
    context.driver.find_element(By.XPATH, select_component_xpath(component_id)).click()
    time.sleep(1)
    assert not context.driver.find_elements(By.XPATH, select_component_option_xpath(option))


@then('the select component with id "{component_id}" will have the "{value}" item selected')
@wait_at_most(2, SECOND)
def step_impl(context, component_id, value):
    assert context.driver.find_element(By.XPATH,
                                       f"{select_component_xpath(component_id)}//span[@class='v-select__selection-text']").text == value
