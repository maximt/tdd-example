import re
import time
import os
import imaplib
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

        start = time.time()
        imap = imaplib.IMAP4_SSL('imap.yandex.ru')
        try:
            imap.login(test_email, os.environ['EMAIL_PASSWORD'])
            while (time.time() - start) < 120:
                imap.select('INBOX')
                typ, data = imap.search(None, 'ALL')
                for msg_id in data[0].split():
                    _, raw_data = imap.fetch(msg_id, '(RFC822)')
                    msg_data = raw_data[0][1].split(b'\r\n')
                    lines = [l.decode('latin-1') for l in msg_data]
                    for l in lines:
                        if f'Subject: {subject}' in l:
                            body = '\n'.join(lines)
                            imap.store(msg_id, '+FLAGS', '\\Deleted')
                            return body
                time.sleep(5)
        finally:
            # imap.close()
            imap.logout()

    def test_can_get_email_link_to_login(self):
        if self.staging_server:
            test_email = 'vbmax@yandex.ru'
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

