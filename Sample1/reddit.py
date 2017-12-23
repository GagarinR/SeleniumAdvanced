# Basic test without Object Model

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

s1 = 'nonfiction'
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://www.reddit.com/')
driver.find_element_by_xpath('//*[@id="search"]/input[1]').send_keys(s1)
driver.find_element_by_xpath('//*[@id="search"]/input[2]').click()
page = 0
driver.implicitly_wait(1)
#-------------------------
arr= driver.find_elements_by_xpath("(//*[@class = 'contents'])[2]//*[@class='search-result-header']/a")
for i in arr:
        print s1 in i.text
page += 1
print 'page: ', page
#-------------------------
if driver.find_element_by_xpath("(//*[@class='nextprev'])[2]/a").is_displayed():
    driver.find_element_by_xpath("(//*[@class='nextprev'])[2]/a").click()

    try:
        while driver.find_element_by_xpath("//*[@class='nextprev']/a[2]").is_displayed():

            arr= driver.find_elements_by_xpath("//*[@class = 'contents']//*[@class='search-result-header']/a")
            for i in arr:
                print s1 in i.text

            page += 1
            print 'page: ', page
            driver.find_element_by_xpath("//*[@class='nextprev']/a[2]").click()
            driver.implicitly_wait(2)

    except NoSuchElementException:
            print 'Last Page: ', page







