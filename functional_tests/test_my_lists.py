from django.conf import settings
from django.contrib.auth import get_user_model
from .management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server
from .base import FunctionalTest


User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        # visit any page to set a cookies
        self.browser.get(self.live_server_url + '/404_url')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session('test@test.test')

        # start new list
        self.browser.get(self.live_server_url)
        self.add_list_item('Splines')
        self.add_list_item('Eschaton')
        url_list_first = self.browser.current_url

        # go to My Lists page
        self.browser.find_element_by_link_text('My lists').click()

        # this is my list?
        self.wait_for(lambda: self.browser.find_element_by_link_text('Splines'))
        self.browser.find_element_by_link_text('Splines').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, url_list_first))

        # create another list
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        url_list_second = self.browser.current_url

        # new list is here?
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(lambda: self.browser.find_element_by_link_text('Click cows'))
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, url_list_second))

        # log out
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_elements_by_link_text('My lists'), []))

