import re
import time
import os
import  poplib
from selenium.webdriver.common.keys import Keys
from django.core import mail
from .base import FunctionalTest


SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop3.promsvyaz.pro')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['EMAIL_PASSWORD'])

            while (time.time() - start) < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('Getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if f'Subject: {subject}':
                        email_id = i
                        body = '\n'.join(lines)
                        return body

        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_login(self):
        if self.staging_server:
            test_email = 'monitor@promsvyaz.pro'
        else:
            test_email = 'test@test.test'

        self.browser.get(self.live_server_url)

        # send email
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # email sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # check sent email
        body = self.wait_for_email(test_email, SUBJECT)
        self.assertIn('Use this link to log in', body)
        url_search = re.search('http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email:\n{body}')
        url_login = url_search.group(0)
        self.assertIn(self.live_server_url, url_login)

        # check login url
        self.browser.get(url_login)

        # check is logged in
        self.wait_to_be_logged_in(email=test_email)

        # log out now
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out(email=test_email)

