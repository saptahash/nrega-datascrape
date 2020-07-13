import selenium
#from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

import time


nrega_url = "https://nregarep2.nic.in/netnrega/dynamic2/dynamicreport_new4.aspx"


def scrape_report(state, labour_month, year):
    mime_types = ['text/plain', 
    'application/vnd.ms-excel', 
    'text/csv', 
    'application/csv', 
    'text/comma-separated-values', 
    'application/download', 
    'application/octet-stream', 
    'binary/octet-stream', 
    'application/binary', 
    'application/x-unknown',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    year_limits = str(year) + '-' + str(year+1)
    if(state < 10):
        state_ID = '0' + str(state)
    else:
        state_ID = str(state)
#    profile = selenium.webdriver.FirefoxProfile()
#    profile.set_preference('browser.download.folderList', 2) # custom location
#    profile.set_preference("browser.download.dir", r'C:\Users\sapta\Downloads\datasets\nrega\working')
#    profile.set_preference('browser.download.manager.showWhenStarting', False)
#    profile.set_preference('browser.download.dir', '/tmp')
#    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ",".join(mime_types))
#    #profile.update_preferences()
    options = Options()
    options.set_preference("browser.download.folderList",2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir","/data")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/ms-excel; charset=utf-8")
    driver = selenium.webdriver.Firefox(firefox_options= options, executable_path = 'C:/Users/sapta/Downloads/software/geckodriver-v0.26.0-win64/geckodriver.exe')

#    driver = selenium.webdriver.Firefox(firefox_profile = profile, executable_path = 'C:/Users/sapta/Downloads/software/geckodriver-v0.26.0-win64/geckodriver.exe')
    driver.get(nrega_url)
    # total hh's applied for job card
    driver.find_element_by_xpath("//input[contains(@id,'ChkLstFieldsWorkerA_0')]").click()
    # total job card issues
    driver.find_element_by_xpath("//input[contains(@id,'ChkLstFieldsWorkerA_1')]").click()
    # total hh's demanded work
    driver.find_element_by_xpath("//input[contains(@id,'ChkLstFieldsWorkerC_0')]").click()
    # total persons demanded work
    driver.find_element_by_xpath("//input[contains(@id,'ChkLstFieldsWorkerC_1')]").click()
    # total hh's alloted work
    driver.find_element_by_xpath("//input[contains(@id,'ChkLstFieldsWorkerD_0')]").click()
    # total persons demanded work 
    driver.find_element_by_xpath("//input[contains(@id,'ChkLstFieldsWorkerD_1')]").click()
    # total person-days
    driver.find_element_by_xpath("//input[contains(@id,'ChkLstFieldsWorkerE_13')]").click()
    ####
    ## selecting month for monthwise labour indicators
    ####
    for i in range(5,9):
        x_path_tickbox = "//input[@id='TxtBox" + str(i) + "\']"
        x_path_menu = 'DdlstTxtBox' + str(i)
        driver.find_element_by_xpath(x_path_tickbox).click()
        month = Select(driver.find_element_by_name(x_path_menu))
        month.select_by_visible_text(str(labour_month))
    # total bank accounts
    driver.find_element_by_xpath("//input[contains(@id,'CTxtBox3')]").click()
    # amount disbursed to bank accounts
    driver.find_element_by_xpath("//input[contains(@id,'CTxtBox6')]").click()
    # total post office accounts
    driver.find_element_by_xpath("//input[contains(@id,'CTxtBox7')]").click()
    # amount disbursed to post office accounts
    driver.find_element_by_xpath("//input[contains(@id,'CTxtBox10')]").click()
    # select granularity
    region = Select(driver.find_element_by_name("regionselect"))
    region.select_by_visible_text("Block")
    # select state
    x_path_state = "//input[@value=\'" + state_ID + "\']"
    driver.find_element_by_xpath(x_path_state).click()
    
    year = Select(driver.find_element_by_name("DdlstFinYear"))
    year.select_by_visible_text(year_limits)
    
    driver.find_element_by_id("dwnldDummy").click()
    time.sleep(10)
    driver.quit()

# year range: 2011 - 2019
# state range: 01-32
scrape_report(8, "May", 2014)


