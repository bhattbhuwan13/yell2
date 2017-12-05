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


all_articles = []
businessNames = []
websites = []
all_articles = driver.find_elements_by_css_selector(".businessCapsule")



for article in all_articles:

    # For gettting the website link
    a_website = article.find_elements_by_xpath(".//a[contains(@class,'businessCapsule--ctaItem')]")
    # dummy_site = a_website.find_element_by_class_name('businessCapsule--ctaItem')
    if len(a_website)>0:
        web_link = a_website[-1].get_attribute("href")
        # print(web_link)
        # sys.exit()

        if (web_link != None or " " or ""):
            websites.append(web_link)
        else:
            websites.append("null")
    else:
        websites.append("null")

    # For getting the business name
    a_business = article.find_element_by_xpath(".//a[@class='businessCapsule--name']")
    a_business_name = a_business.text
    if a_business_name != None or " " or "":
        businessNames.append(a_business_name)
    else:
        businessNames.append("null")

print(len(all_articles))

for i in range(0,len(all_articles)):
    print(businessNames[i], "\t",websites[i])
