import selenium
#from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import os
import time
import subprocess
import concurrent.futures
from itertools import repeat
import bs4
import requests
import shutil
import glob
import pathlib

pwd = "data"
nrega_url = "https://nregarep2.nic.in/netnrega/dynamic2/dynamicreport_new4.aspx"
# ddir_unix = "C:/Users/sapta/Downloads/*"
#command = "mv " + ddir_unix + "/report*" + " " + pwd_unix + "/" + str(current_year) + "/" + str(current_month)
#subprocess.run(command , shell = True)


# set working directory
# os.chdir(pwd)


def scrape_report(state, labour_month, year):
    #    mime_types = ['text/plain',
    #    'application/vnd.ms-excel',
    #    'text/csv',
    #    'application/csv',
    #    'text/comma-separated-values',
    #    'application/download',
    #    'application/octet-stream',
    #    'binary/octet-stream',
    #    'application/binary',
    #    'application/x-unknown',
    #    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    year_limits = str(year) + '-' + str(int(year)+1)
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
    options.add_argument('-headless')
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", os.path.abspath(pwd))
#    directory = "C:/Users/sapta/OneDrive/Desktop/projects/dissertation/codes/nrega_datascrape/nrega-datascrape/data"
#    print(directory)
    options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/ms-excel; charset=utf-8")
    driver = selenium.webdriver.Firefox(
        firefox_options=options, executable_path='geckodriver.exe')

#    driver = selenium.webdriver.Firefox(firefox_profile = profile, executable_path = 'C:/Users/sapta/Downloads/software/geckodriver-v0.26.0-win64/geckodriver.exe')
#    set_download_dir(driver, directory)
    try:
        driver.get(nrega_url)
        time.sleep(10)
#    except TimeoutException:
#        time.sleep(10)
#        driver.get(nrega_url)
#        time.sleep(20)
    except:
        print("failed: shutting down driver")
        driver.quit()
    # total hh's applied for job card
    driver.find_element_by_xpath(
        "//input[contains(@id,'ChkLstFieldsWorkerA_0')]").click()
    # total job card issues
    driver.find_element_by_xpath(
        "//input[contains(@id,'ChkLstFieldsWorkerA_1')]").click()
    # total hh's demanded work
    driver.find_element_by_xpath(
        "//input[contains(@id,'ChkLstFieldsWorkerC_0')]").click()
    # total persons demanded work
    driver.find_element_by_xpath(
        "//input[contains(@id,'ChkLstFieldsWorkerC_1')]").click()
    # total hh's alloted work
    driver.find_element_by_xpath(
        "//input[contains(@id,'ChkLstFieldsWorkerD_0')]").click()
    # total persons demanded work
    driver.find_element_by_xpath(
        "//input[contains(@id,'ChkLstFieldsWorkerD_1')]").click()
    # total person-days
    driver.find_element_by_xpath(
        "//input[contains(@id,'ChkLstFieldsWorkerE_13')]").click()
    ####
    # selecting month for monthwise labour indicators
    ####
    for i in range(5, 9):
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
    print(f"Finished scraping {state} for {labour_month} in {year}")
    # time.sleep(3)
    driver.quit()


# year range: 2011 - 2019
# state range: 01..05-33-06..08-10..14-34

months = ['January', 'February',  'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
years = ["2015", "2016", "2017"]

# , "2014", "2015", "2016", "2017", "2018", "2019"] -> doing only three years for now

# How to pass multi arg functions to map
# https://yuanjiang.space/threadpoolexecutor-map-method-with-multiple-parameters
######################################################
############ SCRAPE STATES IN CODE!!!!!!! #################
###############################################
#driver = selenium.webdriver.Firefox(firefox_options= options, executable_path = 'C:/Users/sapta/Downloads/software/geckodriver-v0.26.0-win64/geckodriver.exe')

#html_content = requests.get(nrega_url).text
#soup_alt = bs4.BeautifulSoup(html_content, 'lxml')
# soup_alt.find_all("statebox")

states = [1, 2, 3, 4, 5, 33, 7, 8, 10, 11, 12, 13, 14, 34, 15, 16,
          19, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 35, 32]


months = ['January', 'February']
states = [1, 2, 3]
years = ["2015"]

pathlib.Path(pwd).mkdir(parents=True, exist_ok=True)
for current_year in years:
    for current_month in months:
        with concurrent.futures.ThreadPoolExecutor(11) as executor:
            interlist = executor.map(scrape_report, states, repeat(
                current_month), repeat(current_year))
        pwd_unix = os.path.join("data", str(current_year), str(current_month))
        pathlib.Path(pwd_unix).mkdir(
            parents=True, exist_ok=True)
        file_list = [f for f in os.listdir(
            pwd) if os.path.isfile(os.path.join(pwd, f))]
        for file in file_list:
            shutil.move(os.path.join(pwd, file), pwd_unix)

# RUN TILL HERE
#scrape_report(3, "May", 2014)
#ddir = "/mnt/c/Users/sapta/Downloads/report*"
#os.system(f"mv {ddir} {pwd}")
#os.popen(f"mv {ddir} {pwd}")
#subprocess.call(["mv", ddir, pwd], shell  = True)

# mv C:/Users/sapta/Downloads/report* ./data
