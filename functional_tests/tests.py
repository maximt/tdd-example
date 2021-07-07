from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
import time
import unittest


WAIT_MAX = 5

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        url = os.environ.get('STAGING_SERVER')
        if url:
            self.live_server_url = 'http://' + url

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            row_text, 
            [row.text for row in rows]
        )

    def wait_for_element(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(
                    row_text, 
                    [row.text for row in rows]
                )
                return
            except (AssertionError, WebDriverException) as e:
                if (time.time() - start_time) > WAIT_MAX:
                    raise e
                time.sleep(0.5)

    def test_can_start_list_for_one_user(self):
        self.browser.get(self.live_server_url)

        # is this main page?
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # create new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter item'
        )
        inputbox.send_keys('Buy feathers')
        inputbox.send_keys(Keys.ENTER)
        
        # check is item created
        self.wait_for_element('1: Buy feathers')

        # create another item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Make fly')
        inputbox.send_keys(Keys.ENTER)

        # check is all items created
        self.wait_for_element('1: Buy feathers')
        self.wait_for_element('2: Make fly')
        
        # self.fail('End test')

    def test_multiple_users_can_start_different_urls(self):
        # user 1

        self.browser.get(self.live_server_url)

        # create new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter item'
        )
        inputbox.send_keys('Buy feathers')
        inputbox.send_keys(Keys.ENTER)

        # check is item created
        self.wait_for_element('1: Buy feathers')

        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+')

        # user 2

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy feathers', page_text)
        self.assertNotIn('Make fly', page_text)

        # create new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter item'
        )
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # check is item created
        self.wait_for_element('1: Buy milk')

        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy feathers', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_element('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)