# Basic test without Object Model
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from ddt import ddt, data


# Automation is based on several assumptions:
# 1) In task it's said that "nonfiction" string should be present in every title. 
# Taking in consideration that "nonfiction" is taken in quotes, we will search for lowercase "nonfiction"
# Which means that resultst which begin with uppercase "Nonfiction" will fail the test
# 2) Meaningfull logging was added in case of failure;
# 3) Added method for explicit wait to speed up the test;
# 4) Made test to be data driven. Please note, that it's still verifying exact search string presence in title

# Additional Info:
# to launch: pytest reddit-bogdan.py --no-print-logs
# In case we need to match lower case and upper case search string in title of result,
# I would use regular expressions


@ddt
class TestReddit(unittest.TestCase):

    def explicitly_wait_for_element_by_xpath(self, element_xpath, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, element_xpath)))
        except (NoSuchElementException, TimeoutException):
            raise NoSuchElementException(
                'Element was not located by xpath "{}" within {} seconds'.
                format(element_xpath, timeout))

    def setUp(self):
        self.test_string = 'nonfiction'
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.get('https://www.reddit.com/')
        self.driver = driver
        print("print endo fo setup")
        # defining xpaths
        self.search_box = '//input[@name="q"]'   # usage of unique attributes of element is preferrable to their order: //*[@id="search"]/input[1]
        self.search_lens = '//input[@type="submit"]'
        self.results_xpath = '(//*[@class = "contents"])[last()]//*[@class="search-result-header"]/a'
        self.search_header_label = '//*[@class="search-header-label"]'
        self.footer_bottom = '(//*[@class = "nav-buttons"])[last()]'
        self.next_page_bottom = '(//*[@rel="nofollow next"])[last()]'

    def tearDown(self):
        self.driver.quit()

    @data('alsdnflkf fdeni', 'nonfiction')
    def test_search(self, search_string):
        driver = self.driver
        driver.find_element_by_xpath(self.search_box).send_keys(search_string)
        driver.find_element_by_xpath(self.search_lens).click()
        search_results_that_do_not_contain_searchsting = []
        current_page = 1
        while True:
            # We need to wait until page with results were loaded:
            self.explicitly_wait_for_element_by_xpath(self.search_header_label)

            # In case there're no search results we raise exception.
            search_results = driver.find_elements_by_xpath(self.results_xpath)
            if len(search_results) == 0:
                raise Exception('Search by string "{}" did not\
                return results. Failing the test. Current_page: {}'.format(search_string, current_page))

            # Verifying that search string is in each title
            for element in search_results:
                current_search_result = element.text
                if not search_string in current_search_result:
                    search_results_that_do_not_contain_searchsting.append("{}\n".format(current_search_result))

            try:
                next_button = driver.find_element_by_xpath(self.next_page_bottom)
            except NoSuchElementException:
                break
            if next_button.is_enabled():
                next_button.click()
                current_page += 1
            else:
                break
        # Test passes if all search results have the string:
        num_of_search_results_that_do_not_contain_searchsting = len(search_results_that_do_not_contain_searchsting)
        assert num_of_search_results_that_do_not_contain_searchsting == 0,\
            'List of results that did not contain search string "{}":\n {}'.\
            format(search_string, search_results_that_do_not_contain_searchsting)
