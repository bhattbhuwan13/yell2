import sys
import time
import pandas as pd
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

WAITING_TIME=5
RANDOM_WAITING_TIME = randint(5, 8)
PAGE_LOAD_TIME = 30
# driver = webdriver.Chrome('/Users/bhuwanbhatt/Downloads/chromedriver')
driver = webdriver.Safari()
driver.get("http://www.yell.com")
elem = driver.find_element_by_name("location")
elem.clear()
elem.send_keys("london")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source



businessNames = []
websites = []
phoneNumbers=[]
categoryNames=[] #Name of the category
categories_element=[]

categories_element = driver.find_elements_by_css_selector('.home--popularSearchesList div:nth-of-type(2) div li a')

# Use this list k/a categories_element to extract category name
fileName= categories_element[0].text

# Getting the link of each occupational category
categories_links = [x.get_attribute("href") for x in categories_element]

# Remove all the location links from the categories_links

for link in categories_links:
    time.sleep(RANDOM_WAITING_TIME)
    driver.get(link)
    print(driver.title)
    break



# driver.implicitly_wait(WAITING_TIME) # seconds
get_london = driver.find_element_by_partial_link_text("London")
# print(get_london.text)

link_is = get_london.get_attribute("href")

driver.implicitly_wait(WAITING_TIME) # seconds
time.sleep(RANDOM_WAITING_TIME)
driver.set_page_load_timeout(PAGE_LOAD_TIME)
driver.get(link_is)


# Getting pagination links
pagination_links_elements=[]
time.sleep(3)
pagination_links_elements = driver.find_elements_by_css_selector('.pagination div:nth-of-type(2) a')



pagination_links = [link.get_attribute("href") for link in pagination_links_elements]


def scrape_page():
    """
    This function is used to scrape data inside a page after the occupation category and location is entered.
    """

    all_articles = []
    time.sleep(RANDOM_WAITING_TIME)
    all_articles = driver.find_elements_by_css_selector(".businessCapsule")



    for article in all_articles:

        # For gettting the website link
        # time.sleep(RANDOM_WAITING_TIME)
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

        # time.sleep(RANDOM_WAITING_TIME)
        # For getting the business name
        a_business = article.find_element_by_xpath(".//a[@class='businessCapsule--name']")
        a_business_name = a_business.text
        if a_business_name != None or " " or "":
            businessNames.append(a_business_name)
        else:
            businessNames.append("null")

        # time.sleep(RANDOM_WAITING_TIME)
        # For getting the phone number
        a_phone = article.find_element_by_xpath(".//span[@class='business--telephoneNumber']")
        a_phoneNumber = a_phone.text
        if a_phone != None or " " or "":
            phoneNumbers.append(a_phoneNumber)
        else:
            phoneNumbers.append("null")


        a_category_name = driver.find_element_by_name("keywords")
        a_category = a_category_name.get_attribute("value")
        if a_category_name != None or " " or "":
            categoryNames.append(a_category)
        else:
            categoryNames.append("null")

def createCSV(name,website,phone,category):
    all_businesses = {
    'Business Name':name,
    'Website':website,
    'Phone':phone,
    'Business Type':category
    }
    df = pd.DataFrame(all_businesses,columns=['Business Name','Website','Phone','Business Type'])
    df.to_csv('yellNew.csv',index = False)

scrape_page()
createCSV(businessNames,websites,phoneNumbers,categoryNames)
sys.exit()
# for links in pagination_links_elements:
#     driver.implicitly_wait(WAITING_TIME) # seconds
#     links.click()
#     scrape_page()
# i = 1
for link in pagination_links:
    # i = i + 1
    time.sleep(RANDOM_WAITING_TIME)
    driver.implicitly_wait(WAITING_TIME)
    driver.set_page_load_timeout(PAGE_LOAD_TIME)
    driver.get(link)
    scrape_page()
createCSV(businessNames,websites,phoneNumbers)
