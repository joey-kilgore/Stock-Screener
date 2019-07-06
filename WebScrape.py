import csv
import parameters
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

driver = None
optionsDict = {}

# function to ensure all key data fields have a value
def validate_field(field):
    # if field is present pass if field:
    if field:
        pass
    # if field is not present print text else:
    else:
        field = 'No results'
    return field

def setupDriver():
    global optionsDict
    # load options from csv file
    
    with open('options.csv','r') as f:
        line = f.readline()
        while line:
            parts = line.split(',', 1)
            optionsDict[parts[0]] = parts[1]
            line = f.readline()

    global driver
    # specifies the path to the chromedriver.exe
    driver = webdriver.Chrome('C:/Users/Joey/Downloads/Install Files/chromedriver_win32/chromedriver.exe')

    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://finviz.com/screener.ashx?v=111')

    sleep(1)

def printTickers(option):
    global driver
    global optionsDict
    driver.get(optionsDict[option])

    tickerElements = driver.find_elements_by_class_name("screener-link-primary")
    textTickers = []
    for ticker in tickerElements:
        print(ticker.text)
        textTickers.append(ticker.text + ' ')

    return textTickers

def setOption(link, name):
    global optionsDict

    with open('options.csv','a') as fd:
        row = name +','+link
        fd.writelines(row+'\n')

    optionsDict[name] = link

def removeOption(name):
    global optionsDict
    del optionsDict[name]
    with open("options.csv", "r") as f:
        lines = f.readlines()
    with open("options.csv", "w") as f:
        for line in lines:
            print(line)
            print(line.split(",",1))
            if line.split(",",1)[0] != name:
                f.write(line)

def getOptions():
    global optionsDict
    if optionsDict.keys():
        return optionsDict.keys()
    else:
        return "There are no current options setup use !setOptions to set a new option"

def quitDriver():
    driver.quit()

setupDriver()