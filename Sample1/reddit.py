# Basic test without Object Model

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

s1 = 'nonfiction'
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://www.reddit.com/')
driver.find_element_by_xpath('//*[@id="search"]/input[1]').send_keys(s1)  # better to use unique attributes, see my test
driver.find_element_by_xpath('//*[@id="search"]/input[2]').click()
page = 0
driver.implicitly_wait(1) #implicit wait is unreliable, better to use explicit wait.
# ------------------------- To keep it clean and tidy, this has to go inside the loop
# Problem was that locators on first page and on second + pages are different
# In this case it's better to use "last()" xpath function. For example: 
"(//*[@class = 'contents'])[last()]//*[@class='search-result-header']/a"
arr = driver.find_elements_by_xpath("(//*[@class = 'contents'])[2]\
    # //*[@class='search-result-header']/a") # need to use better naming (i know it's just a mockup, but still)
for i in arr:
        print(s1 in i.text)
page += 1
print('page: ', page)
# -------------------------
if driver.find_element_by_xpath("(//*[@class='nextprev'])[2]/a").is_displayed():
    driver.find_element_by_xpath("(//*[@class='nextprev'])[2]/a").click()

    try:
        # Let's say, we hit the last page. "Next" button won't be displayed. But the results will be displayed, right?
        # In this case, your while loop will finish before checking results on last page
        while driver.find_element_by_xpath("//*[@class='nextprev']/a[2]").is_displayed():

            arr= driver.find_elements_by_xpath("//*[@class = 'contents']//*[@class='search-result-header']/a") # naming convention
            for i in arr: # variable naming
                print(s1 in i.text)

            page += 1
            print('page: ', page)
            driver.find_element_by_xpath("//*[@class='nextprev']/a[2]").click()
            driver.implicitly_wait(2) # Implicitly wait is detemined for whole test. It can be determined once. Somewhere on top.
            # I assume you wanted just to sleep 2 seconds here, but I think it will sleep for all commands.

    except NoSuchElementException:
            print('Last Page: ', page)







