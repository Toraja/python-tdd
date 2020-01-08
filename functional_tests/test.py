from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT_SEC = 10
INTERVAL_SEC = 0.5


class NewVisitorTest(LiveServerTestCase):
    """TODO write description"""
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        input('Press Enter to continue...')
        self.browser.quit()

    def run_func_until_time_has_passed(self, max_wait_sec, interval_sec, func,
                                       arg_list):
        start_time = time.time()

        def time_has_passed():
            if time.time() - start_time > max_wait_sec:
                return True
            return False

        while True:
            try:
                func(*arg_list)
                return
            except (AssertionError, WebDriverException) as e:
                if time_has_passed():
                    raise e
                time.sleep(interval_sec)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # She types "Buy peacock feathers" into a text box
        # (Edith's hobby is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-to list
        inputbox.send_keys(Keys.ENTER)
        self.run_func_until_time_has_passed(MAX_WAIT_SEC, INTERVAL_SEC,
                                            self.check_for_row_in_list_table,
                                            ['1:Buy peacock feathers'])

        # There is still a text box invinting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, now shows both items on her list
        self.run_func_until_time_has_passed(MAX_WAIT_SEC, INTERVAL_SEC,
                                            self.check_for_row_in_list_table,
                                            ['1:Buy peacock feathers'])
        self.run_func_until_time_has_passed(
            MAX_WAIT_SEC, INTERVAL_SEC, self.check_for_row_in_list_table,
            ['2:Use peacock feathers to make a fly'])

        # Edith wonder whether the site will remember the list.
        # Then she sees that the site has generated a unique URL for her --
        # there is explanatory text for that effect.
        self.fail('Finish the test!')

        # She visits the URL -- her to-do list is still there.

        # Satisfied, she goes back to sleep.
