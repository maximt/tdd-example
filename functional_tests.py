from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            row_text, 
            [row.text for row in rows]
        )

    def test_start_and_retrieve_list(self):
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        # create another item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Make fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # check is all items created

        self.check_for_row_in_list_table('1: Buy feathers')
        self.check_for_row_in_list_table('2: Make fly')

        # self.fail('End test')


if __name__ == '__main__':
    unittest.main()
