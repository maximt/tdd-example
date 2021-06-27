from selenium import webdriver
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
        self.fail('End test')

        #todo: start list


if __name__ == '__main__':
    unittest.main()
