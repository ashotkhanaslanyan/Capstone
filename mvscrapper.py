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
import time
from bs4 import BeautifulSoup
import requests
import helpers as hp
import math

# columns = ['Name', 'Club', 'League', 'Season', 'Market Value', "tm_Id"]
# mvs = hp.create_or_open("./Scrapped_Data/markval.csv", columns)


def scrap_mvs(link, driver, start=2005, end=2020):
    for season in range(start, end):
        try:
            print("getting mvs for " + str(season))
            link = link[:-4] + str(season)
            driver.get(link)
            bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
            table = bs_obj.find_all('table')[1]
            def get_id(input): return input["id"]
            a = table.find_all('a', class_="spielprofil_tooltip tooltipstered")
            ids = list(map(get_id, a))
            mv_season = str(season)[-2:] + '/' + str(season + 1)[-2:]
            df = pd.read_html(str(table))[0]
            df = df[["#", "Player", "Market value"]]
            df = df[df['#'].notna()]
            df = df.drop(["#"], axis=1)
            df.columns = ["Name", "Market Value"]
            club = driver.find_element_by_xpath(
                "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataName', ' ' ))]//span").text
            league = driver.find_element_by_xpath(
                "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hauptpunkt', ' ' ))]//a").text
            df.insert(1, "Club", club)
            df.insert(2, "League", league)
            df.insert(3, "Season", mv_season)
            df.insert(5, "tm_Id", ids[::2])
            df.set_index("tm_Id", drop = False, inplace = True)
            df.to_csv("Scrapped_Data/markval.csv", mode = 'a', header = False)
        except Exception as e:
            print(str(e))


opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)

team_links = pd.read_csv("Prerequisit Data/teamlinks.csv")["Team_url"]

start = 4
end = 8
if(not(hp.check_if_exists("Scrapped_Data/markval.csv"))):
    hp.create_empty_df("Scrapped_Data/markval.csv", columns = ['Name', 'Club', 'League', 'Season', 'Market Value', "tm_Id"])
for team in range(start, end):
    try:
        link = team_links[team]
        scrap_mvs(link=link, driver=driver, start = 2010, end = 2012)
    except Exception as e:
        print(str(e))
        driver.quit()

driver.quit()