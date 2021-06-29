from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


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

        # check is item created
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy feathers' for row in rows),
            'New item not added'
        )

        #todo create another item

        self.fail('End test')


if __name__ == '__main__':
    unittest.main()
