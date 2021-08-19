from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_list_for_one_user(self):
        self.browser.get(self.live_server_url)

        # is this main page?
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # create new item
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter item'
        )
        self.add_list_item('Buy feathers')

        # create another item
        self.add_list_item('Make fly')
        # check is all items created
        self.wait_for_element('1: Buy feathers')
        self.wait_for_element('2: Make fly')
        
        # self.fail('End test')

    def test_multiple_users_can_start_different_urls(self):
        # user 1

        self.browser.get(self.live_server_url)

        # create new item
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter item'
        )
        self.add_list_item('Buy feathers')

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
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter item'
        )

        self.add_list_item('Buy milk')

        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy feathers', page_text)
        self.assertIn('Buy milk', page_text)
