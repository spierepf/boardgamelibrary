from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .behave_layer import BehaveLayer


class SeleniumLayer(BehaveLayer):
    def before_all(self, context):
        options = Options()
        options.headless = True
        context.driver = webdriver.Chrome(options)

    def after_all(self, context):
        context.driver.quit()
