from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.firefox.options import Options
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import time
import helpers as hp
import functools
import re
import requests 

opts = Options()
opts.headless = False
driver = webdriver.Firefox(options=opts)

countries_df = pd.DataFrame({'countries':[], 'leageues':[]})
dicts = []

for i in range(0,194):
    link = "https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/" + str(i)
    try:
        driver.get(link)
        country = driver.find_element_by_xpath('//*[(@id = "land_select_breadcrumb_chzn")]//span').text
        leagues = driver.find_elements_by_xpath('//*[(@id = "yw1")]//a')
        leagues = list(map(lambda x: x.text, leagues))
        leagues = list(filter(lambda x: x!= "", leagues))
        diction = {
            "countries" : country,
            "leagues": leagues
        }
        dicts.append(diction)
    except Exception as e: 
        print(link)
        print(str(e))

driver.quit()

for diction in dicts:
    countries_df = countries_df.append(diction, ignore_index = True)

countries_df.to_pickle("countries.pkl")