import csv
import parameters
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

# function to ensure all key data fields have a value
def validate_field(field):
    # if field is present pass if field:
    if field:
        pass
    # if field is not present print text else:
    else:
        field = 'No results'
    return field

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('C:/Users/Joey/Downloads/Install Files/chromedriver_win32/chromedriver.exe')

# driver.get method() will navigate to a page given by the URL address
driver.get('https://finviz.com/screener.ashx?v=111')

sleep(1)

oSelect = driver.find_element_by_id('fs_exch')
options = [x for x in oSelect.find_elements_by_tag_name("option")]
for option in options:
    print(option.get_attribute("value") + ' ' + option.text)

print("")

tickerElements = driver.find_elements_by_class_name("screener-link-primary")
for ticker in tickerElements:
    print(ticker.text)

driver.quit()