from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)

        # send empty item
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # wait for error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'You cant have empty list item'
        ))

        # send new item
        self.browser.find_element_by_id('id_new_item').send_keys('buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_element('1: buy milk')

        # send empty again
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # wait for error message again
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'You cant have empty list item'
        ))

        # send new item again
        self.browser.find_element_by_id('id_new_item').send_keys('make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        self.wait_for_element('1: buy milk')
        self.wait_for_element('2: make tea')

        self.fail('todo')
