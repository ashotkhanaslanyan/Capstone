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

columns = ['Name', 'Club', 'League', 'Season', 'Market Value', "tm_Id"]
mvs = hp.create_or_open("./Scrapped_Data/Mvs.csv", columns)

def scrap_mvs(link, driver, start = 2005, end = 2020):
    team_df = pd.DataFrame(columns = ['Name', 'Club', 'League', 'Season', 'Market Value', "tm_Id"])
    try:
        for season in range(start, end):
            print("getting mvs for " + str(season))
            link = link[:-4] + str(season)
            driver.get(link)
            bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
            table = bs_obj.find_all('table')[1]
            get_id = lambda input : input["id"]
            a = table.find_all('a', class_ ="spielprofil_tooltip tooltipstered")
            ids = list(map(get_id,a))
            mv_season = str(season)[-2:] + '/' + str(season + 1)[-2:]
            df = pd.read_html(str(table))[0]
            df = df[["#","Player","Market value"]]
            df = df[df['#'].notna()]
            df = df.drop(["#"], axis = 1)
            df.columns = ["Name", "Market Value"]
            club = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataName', ' ' ))]//span").text
            league = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hauptpunkt', ' ' ))]//a").text
            df.insert(1,"Club", club)
            df.insert(2,"League", league)
            df.insert(3,"Season", mv_season)
            df.insert(5, "tm_Id", ids[::2])
            team_df = team_df.append(df)
    except Exception as e:
        print(str(e))
    return team_df

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options= opts)

team_links = pd.read_csv("Prerequisit Data/teamlinks.csv")["Team_url"]

start = 0; end = 1
df = pd.DataFrame(columns = ['Name', 'Club', 'League', 'Season', 'Market Value', "tm_Id"])

for team in range(start, end):
    try:
        link = team_links[team]
        mvs_df = scrap_mvs(link = link, driver = driver)
    except Exception as e:
        print(str(e))
        print("writting to csv stopped at", str(mvs.tail(1)["tm_Id"]))
        mvs_df.to_csv("Scrapped_Data/marval.csv")
        driver.quit()

driver.quit()
mvs_df.to_csv("Scrapped_Data/marval.csv")
