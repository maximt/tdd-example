import re
from selenium.webdriver.common.keys import Keys
from django.core import mail
from .base import FunctionalTest


TEST_EMAIL = 'test@test.ts'
SUBJECT = 'Superlists: Your login link'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_login(self):
        self.browser.get(self.live_server_url)

        # send email
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # email sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # check sent email
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)
        self.assertIn('Use this link to log in:', email.body)

        url_search = re.search('http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email:\n{email.body}')
        url_login = url_search.group(0)
        self.assertIn(self.live_server_url, url_login)

        # check login url
        self.browser.get(url_login)

        # check is logged in
        links = self.wait_for(lambda: self.assertTrue(
            self.browser.find_elements_by_link_text('Log out')
        ))
        print( links)
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

