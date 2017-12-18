import sys
import time
import pandas as pd
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities

time.sleep(15)
WAITING_TIME=0
RANDOM_WAITING_TIME = randint(13, 18)
SIMPLE_WAITING_TIME = randint(4, 8)
PAGE_LOAD_TIME = 60
INITIAL = 49
FINAL = INITIAL+1

root = 'csv'
driver = webdriver.Chrome('/Users/bhuwanbhatt/Downloads/chromedriver')
# driver = webdriver.Safari()

# desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
# desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'AppleWebKit/537.36 (KHTML, like Gecko) '
# driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)

time.sleep(RANDOM_WAITING_TIME)

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
fileName= categories_element[INITIAL].text
# print(fileName)
# Getting the link of each occupational category
categories_links = [x.get_attribute("href") for x in categories_element]
# print(categories_links[0:1])


def scrape_page():
    """
    This function is used to scrape data inside a page after the occupation category and location is entered.
    """

    all_articles = []
    #time.sleep(RANDOM_WAITING_TIME)
    all_articles = driver.find_elements_by_css_selector(".businessCapsule")
    a_category_name = driver.find_element_by_name("keywords")
    a_category = a_category_name.get_attribute("value")


    for article in all_articles:

        try:
            a_website = article.find_elements_by_xpath(".//a[contains(@class,'businessCapsule--ctaItem')]")
        except:
            a_website=[]

        if len(a_website)>0:
            web_link = a_website[-1].get_attribute("href")

            if (web_link != None or " " or ""):
                websites.append(web_link)
            else:
                websites.append("null")
        else:
            websites.append("null")

        a_business = article.find_element_by_xpath(".//a[@class='businessCapsule--name']")
        a_business_name = a_business.text
        if a_business_name != None or " " or "":
            businessNames.append(a_business_name)
        else:
            businessNames.append("null")
        try:
            a_phone = article.find_element_by_xpath(".//span[@class='business--telephoneNumber']")
            a_phoneNumber = a_phone.text
        except:
            a_phone = ""
            a_phoneNumber = "null"
        if a_phone != None or " " or "":
            phoneNumbers.append(a_phoneNumber)
        else:
            phoneNumbers.append("null")



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
    df.to_csv(root + '/'+ fileName + '.csv',index = False)


for link in categories_links[INITIAL:FINAL]:
    # driver.implicitly_wait(WAITING_TIME) # seconds
    time.sleep(RANDOM_WAITING_TIME)
    driver.set_page_load_timeout(PAGE_LOAD_TIME)
    driver.get(link)



    # driver.implicitly_wait(WAITING_TIME) # seconds
    get_london = driver.find_element_by_partial_link_text("London")
    # print(get_london.text)

    link_is = get_london.get_attribute("href")

    driver.implicitly_wait(WAITING_TIME) # seconds
    #time.sleep(RANDOM_WAITING_TIME)
    driver.set_page_load_timeout(PAGE_LOAD_TIME)
    driver.get(link_is)


    # Getting pagination links
    pagination_links_elements=[]
    #time.sleep(3)
    pagination_links_elements = driver.find_elements_by_css_selector('.pagination div:nth-of-type(2) a')


    time.sleep(SIMPLE_WAITING_TIME)
    pagination_links = [link.get_attribute("href") for link in pagination_links_elements]
    scrape_page()

    for link in pagination_links:
        # driver.implicitly_wait(WAITING_TIME)
        time.sleep(SIMPLE_WAITING_TIME)
        driver.set_page_load_timeout(PAGE_LOAD_TIME)
        driver.get(link)
        scrape_page()
        time.sleep(RANDOM_WAITING_TIME)

createCSV(businessNames,websites,phoneNumbers,categoryNames)
driver.quit()
