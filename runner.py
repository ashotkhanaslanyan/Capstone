from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.firefox.options import Options
from notify_run import Notify
import numpy as np
import pandas as pd
from csv import writer
import time
import csv
import players as pl
import helpers as hp
import sys
import instasignin as inst

# print(sys.argv[0], sys.argv[1], sys.argv[2])

notify = Notify()
notify.register()
print(notify.info())


opts = Options()
opts.headless = False
driver = webdriver.Firefox(options= opts)

def start_scrapping(driver, start, end, player_links):
    dest_cols = {
        "./Scrapped_Data/Players.csv" : ['Id','tm_Id','Name', 'Team', 'Nationality', 'Date of Birth', 'Height', 'Strong Foot', 'Position', 'Joined', 'Contract Expires', 'Followers'],
        "./Scrapped_Data/stats.csv" : ['Player_Id', 'tm_Id', 'Name', 'Team', 'Season', 'Competition', 'Attribute','value'],
        "./Scrapped_Data/natstats.csv" : ["Player_Id", "tm_Id", "Name","National Team","Competition", "Attribute", "value"],
        "./Scrapped_Data/Transfers.csv" : ['Player_Id', "tm_Id", 'Name', 'From', 'To', 'Fee', 'Market Value', 'Season', 'Date']
    }
    for dest,cols  in dest_cols.items():
        if(not(hp.check_if_exists(dest = dest))):
            hp.create_empty_df(file_dest = dest, columns = cols)

    inst.sign_in(driver)
    for id in range(start, end):
        player = None
        try:
            link = player_links[id]
            name = player_names[id]
            dests = list(dest_cols.keys())
            player = pl.Player(id = id, link = link, driver = driver, df_path = dests[0], stats_path = dests[1],
            nat_stats_path = dests[2], transfers_path = dests[3], name = name)
            notify.send(str(id))
        except Exception as e:
            print("The exception message", str(e))
            notify.send(str(e))
            break
        del player
    driver.quit()
    print("Finished scrapping")


player_links = pd.read_csv('Prerequisit Data/playerlinks.csv')['Player_url']
player_names = pd.read_csv('Prerequisit Data/playerlinks.csv')['Name']

def start_end(st, end):
    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    except:
        start = st
        end = end
    return start, end


start,end = start_end(1084,1086)

start_scrapping(driver, start = start, end = end, player_links = player_links)
