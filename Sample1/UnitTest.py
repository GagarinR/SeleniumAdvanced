import unittest
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

tree = ET.parse('req.xml')
root = tree.getroot()

# print (root)

def getSearchValue(pagename,elementkey):
    xpathstr = "./pages/page[@name='"+pagename+"']/element[@Key='"+elementkey+"']"
    print (xpathstr)
    for element in root.findall(xpathstr):
        value = element.find('value').text
        return value

def getSearchBy(pagename,elementkey):
    xpathstr = "./pages/page[@name='"+pagename+"']/element[@Key='"+elementkey+"']"
    # print (xpathstr)
    for element in root.findall(xpathstr):
        value = element.find('searchby').text
        return value

print (getSearchValue("LoginPage","LoginPassword"))
print (getSearchBy("LoginPage","LoginUserName"))

class DemoLogin(unittest.TestCase):
    def setUp(self): # specially for UnitTest
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")

    # def tearDown(self):
    #     self.driver.close()


    def test_anytexthere(self):
        driver = self.driver
        driver.get("http://demo.mahara.org/")
        self.assertIn("Home - Mahara",  driver.title)
        username = driver.find_element_by_id(getSearchValue("LoginPage","LoginUserName"))
        username.send_keys("admin")
        password = driver.find_element_by_id(getSearchValue("LoginPage", "LoginPassword"))
        password.send_keys("MaharaDemo")
        loginbutton=driver.find_element_by_id(getSearchValue("LoginPage","SubmitButton"))
        loginbutton.click()
        profilebutton = driver.find_element_by_xpath("/html/body/header/div/div/div[2]/button[3]/span[2]")
        profilebutton.click()
        print (driver.find_element_by_xpath('//*[@id="navuser"]/li[4]/a/span[2]').text)
        # // *[ @ id = "navuser"] / li[4] / a / span[2]
        # self.assertIn(driver.find_element_by_xpath('//*[@id="navuser"]/li[4]/a/span[2]'),'Log')

if __name__ == "__main__":
    unittest.main()





