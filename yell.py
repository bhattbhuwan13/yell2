import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

WAITING_TIME=5
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
# These lists will hold the data scraped from the site

businessNames = []
websites = []
phoneNumbers=[]

categories_element=[]

categories_element = driver.find_elements_by_css_selector('.home--popularSearchesList div:nth-of-type(2) div li a')
# Use this list k/a categories_element to extract category name
fileName= categories_element[0].text

# Getting the link of each occupational category
categories_links = [x.get_attribute("href") for x in categories_element]

# Remove all the location links from the categories_links


for link in categories_links:
    driver.get(link)
    print(driver.title)
    break



driver.implicitly_wait(WAITING_TIME) # seconds
get_london = driver.find_element_by_partial_link_text("London")
print(get_london.text)

link_is = get_london.get_attribute("href")
driver.implicitly_wait(WAITING_TIME) # seconds
driver.get(link_is)


# Getting pagination links
pagination_links_elements=[]
pagination_links_elements = driver.find_elements_by_css_selector('.pagination div:nth-of-type(2) a')

# for an_element in pagination_links_elements:
#     driver.implicitly_wait(WAITING_TIME)
#     print(an_element)
#     an_element.click()

# sys.exit()
pagination_links = [link.get_attribute("href") for link in pagination_links_elements]
# print(pagination_links)
# sys.exit()

def scrape_page():
    """
    This function is used to scrape data inside a page after the occupation category and location is entered.
    """

    all_articles = []

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

        a_phone = article.find_element_by_xpath(".//span[@class='business--telephoneNumber']")
        a_phoneNumber = a_phone.text
        if a_phone != None or " " or "":
            phoneNumbers.append(a_phoneNumber)
        else:
            phoneNumbers.append("null")



def createCSV(name,website,phone):
    all_businesses = {
    'Business Name':name,
    'Website':website,
    'Phone':phone
    }
    df = pd.DataFrame(all_businesses,columns=['Business Name','Website','Phone'])
    df.to_csv(fileName + '.csv',index = False)

scrape_page()

# for links in pagination_links_elements:
#     driver.implicitly_wait(WAITING_TIME) # seconds
#     links.click()
#     scrape_page()
# i = 1
for link in pagination_links:
    # i = i + 1
    driver.get(link)
    scrape_page()
createCSV(businessNames,websites,phoneNumbers)
