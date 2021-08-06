from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

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

    def test_cannot_add_dublicate_items(self):
        self.browser.get(self.live_server_url)

        # add one
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_element('1: Buy wellies')

        # add two
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # check dubs
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list",
        ))

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)

        # send item
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_element('1: Banter too thick')

        # send second item
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # check error
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # start new input
        self.get_item_input_box().send_keys('a')

        # check that error is gone
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
