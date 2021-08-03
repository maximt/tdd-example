from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)

        # send empty item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # check browser-side validation
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))

        # send new item
        inputbox = self.get_item_input_box()
        inputbox.send_keys('buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_element('1: buy milk')

        # send empty again
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))

        # send new item again
        inputbox = self.get_item_input_box()
        inputbox.send_keys('make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_element('1: buy milk')
        self.wait_for_element('2: make tea')

