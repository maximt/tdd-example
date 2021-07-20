from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
import time

WAIT_MAX = 5


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        url = os.environ.get('STAGING_SERVER')
        if url:
            self.live_server_url = 'http://' + url

    def tearDown(self):
        self.browser.quit()

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

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if (time.time() - start_time) > WAIT_MAX:
                    raise e
                time.sleep(0.5)
