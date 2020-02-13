from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT_SEC = 10
INTERVAL_SEC = 0.5
ID_INPUTBOX = 'id_new_item'


class NewVisitorTest(StaticLiveServerTestCase):

    debug = 'DEBUG_TEST' in os.environ

    def setUp(self):
        self.browser = webdriver.Firefox()
        domain = os.getenv('DOMAIN')
        if domain:
            self.live_server_url = 'http://'+domain

    def tearDown(self):
        if self.debug:
            input('Press Enter to continue...')
        self.browser.quit()

    def retry_assertion(self, timeout_sec, interval_sec, func, **kwargs):
        start_time = time.time()

        def time_has_passed():
            if time.time() - start_time > timeout_sec:
                return True
            return False

        while True:
            try:
                func(**kwargs)
                return
            except (AssertionError, WebDriverException) as e:
                if time_has_passed():
                    raise e
                time.sleep(interval_sec)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id(ID_INPUTBOX)
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # She types "Buy peacock feathers" into a text box
        # (Edith's hobby is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-to list
        inputbox.send_keys(Keys.ENTER)
        self.retry_assertion(MAX_WAIT_SEC,
                             INTERVAL_SEC,
                             self.check_for_row_in_list_table,
                             row_text='1: Buy peacock feathers')

        # There is still a text box invinting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        inputbox = self.browser.find_element_by_id(ID_INPUTBOX)
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, now shows both items on her list
        self.retry_assertion(MAX_WAIT_SEC,
                             INTERVAL_SEC,
                             self.check_for_row_in_list_table,
                             row_text='1: Buy peacock feathers')
        self.retry_assertion(MAX_WAIT_SEC,
                             INTERVAL_SEC,
                             self.check_for_row_in_list_table,
                             row_text='2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id(ID_INPUTBOX)
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.retry_assertion(MAX_WAIT_SEC,
                             INTERVAL_SEC,
                             self.check_for_row_in_list_table,
                             row_text='1: Buy peacock feathers')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.
        '''We use a new browser session to make sure that no information
        of Edith's coming through from cookies etc'''
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new itme.
        # He is less interesting than Edith...
        inputbox = self.browser.find_element_by_id(ID_INPUTBOX)
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.retry_assertion(MAX_WAIT_SEC,
                             INTERVAL_SEC,
                             self.check_for_row_in_list_table,
                             row_text='1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep.

    def test_layout_and_styling(self):
        # Edith goes to the hoem page
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()

        # She notices the input box is nicely centered
        browser_width = self.browser.get_window_size()['width']
        inputbox = self.browser.find_element_by_id(ID_INPUTBOX)
        inputbox_x_cordinate = inputbox.location['x'] + \
            inputbox.size['width']/2
        self.assertAlmostEqual(inputbox_x_cordinate,
                               browser_width / 2, delta=10)

        # She starts a new list and sees the input is nicely centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.retry_assertion(MAX_WAIT_SEC,
                             INTERVAL_SEC,
                             self.check_for_row_in_list_table,
                             row_text='1: testing')
        inputbox = self.browser.find_element_by_id(ID_INPUTBOX)
        inputbox_x_cordinate = inputbox.location['x'] + \
            inputbox.size['width']/2
        self.assertAlmostEqual(inputbox_x_cordinate,
                               browser_width / 2, delta=10)
