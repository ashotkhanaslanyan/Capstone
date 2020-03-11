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
from csv import writer
import time
import csv
import players as pl

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options= opts)

def create_or_open(file_dest, columns):
    data_frame = None
    try:
        data_frame = pd.read_csv(file_dest, index_col = 0)
    except:
        data_frame = pd.DataFrame(columns=columns)
    return data_frame

columns=['Id','Name', 'Team', 'Nationality', 'Date of Birth', 'Height', 'Strong Foot', 'Position', 'Joined', 'Contract Expires', 'Followers']
players_df = create_or_open(file_dest = "./Scrapped_Data/Players.csv", columns = columns)
player_links_data = pd.read_csv('Prerequisit Data/playerlinks.csv')

for row in range(465, 475):
    player = None
    try:
        link = player_links_data['Player_url'][row]
        player = pl.Player(id = row, link = link, driver = driver)
        data = player.data_to_append()
        players_df = players_df.append(data, ignore_index=True)
    except Exception as e:
        print("exception !!! writting to csv stopped at " +  str(players_df.tail(1)["Id"]))
        print("The exception message", str(e))
        players_df.to_csv("./Scrapped_Data/Players.csv")
        break
    del player
players_df.to_csv("./Scrapped_Data/Players.csv")
driver.quit()
