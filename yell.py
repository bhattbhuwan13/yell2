import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Chrome('/Users/bhuwanbhatt/Downloads/chromedriver')
driver = webdriver.Safari()
driver.get("http://www.yell.com")
elem = driver.find_element_by_name("location")
elem.clear()
elem.send_keys("london")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

# required = driver.find_element_by_link_text("Accountants")
# required.click()

categories_element=[]
categories_element = driver.find_elements_by_xpath("//a[@class='home--popularItemLink']")


categories_links = [x.get_attribute("href") for x in categories_element]

# Remove all the location links from the categories_links


for link in categories_links:
    driver.get(link)
    print(driver.title)
    break

get_london = driver.find_element_by_partial_link_text("London")
print(get_london.text)

link_is = get_london.get_attribute("href")
driver.get(link_is)


# Getting the name of the business
businessName = []
# businessName = driver.find_elements_by_xpath("//a[@class='businessCapsule--name']/h2")
# [print(name.text) for name in businessName]
businessName = driver.find_elements_by_xpath("//a[@class='businessCapsule--name']")
[print(name.text) for name in businessName]


# Getting the websites

websites = []
# businessName = driver.find_elements_by_xpath("//a[@class='businessCapsule--name']/h2")
# [print(name.text) for name in businessName]
websites = driver.find_elements_by_css_selector('.businessCapsule--ctas a:nth-of-type(2)')
# print(websites)
websites_links = [x.get_attribute("href") for x in websites]
[print(a) for a in websites_links]


print("Lengths")
print(len(businessName))
print(len(websites))
