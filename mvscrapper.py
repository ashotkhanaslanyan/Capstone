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
import sys
from notify_run import Notify


notify = Notify()
notify.register()
print(notify.info())


def get_team_league(bs_obj):
    try:
        league = bs_obj.find_all('span', class_="hauptpunkt")[0].find('a').get_text().strip()
        name = bs_obj.find_all('h1')[0].get_text().strip()
    except:
        league = "no_info"
        name = "no_info"
    return name, league


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
            club, league = get_team_league(bs_obj)
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
def start_end(st, end):
    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    except:
        start = st
        end = end
    return start, end
start,end = start_end(500,520)

def start_scrapper(start, end):
    if(not(hp.check_if_exists("Scrapped_Data/markval.csv"))):
        hp.create_empty_df("Scrapped_Data/markval.csv", columns = ['Name', 'Club', 'League', 'Season', 'Market Value', "tm_Id"])
    for team in range(start, end):
        try:
            link = team_links[team]
            st = 2005; end = 2020
            print(team)
            notify.send(str(team))
            if(team == 501):
                st = 2015
            scrap_mvs(link=link, driver=driver, start=st, end=end)
        except Exception as e:
            print(str(e))
            notify.send(str(e))
            driver.quit()

start_scrapper(start, end)


driver.quit()