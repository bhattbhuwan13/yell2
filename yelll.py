import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Chrome('/Users/bhuwanbhatt/Downloads/chromedriver')
driver = webdriver.Safari()
driver.get("http://www.yell.com")


occupation = driver.find_element_by_name("keywords")
occupation.clear()

# This code needs to click on Accountants automatically
occupation.send_keys("Accountants")

location = driver.find_element_by_name("location")
location.clear()
location.send_keys("london")
location.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

print(driver.title)
# Getting all the business infromation from the first page

# Getting telephone numbers

# telephone_numbers = []
# driver.implicitly_wait(10) # seconds
# telephone_numbers = driver.find_element_by_class_name("business--telephoneNumber")
