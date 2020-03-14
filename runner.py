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
import helpers as hp
import transfers as tf

opts = Options()
opts.headless = False
driver = webdriver.Firefox(options= opts)


def start_scrapping(driver, start, end, players_df, stats_df, nat_stats_df, transfers_df, player_links, transfer_links):
    for id in range(start, end):
        player = None
        try:
            link = player_links[id]
            transfer_link = transfer_links[id]
            player = pl.Player(id = id, link = link, driver = driver)
            data = player.data
            players_df = players_df.append(data, ignore_index=True)
            stats_df = stats_df.append(player.stats_df)
            nat_stats_df = nat_stats_df.append(player.nat_stats)
            transfers = tf.get_transfers(link = transfer_link, id = id, driver = driver)
            transfers_df = transfers_df.append(transfers)
        except Exception as e:
            print("exception writting to csv, players_df stopped at " +  str(players_df.tail(1)["Id"]))
            print("exception writting to csv, stats stopped at " +  str(stats_df.tail(1)["Player_Id"]))
            print("exception writting to csv, nat_stats stopped at " +  str(nat_stats_df.tail(1)["Player_Id"]))
            print("exception writting to csv, trasnfers stopped at " +  str(transfers_df.tail(1)["Player_Id"]))
            print("The exception message", str(e))
            players_df.to_csv("./Scrapped_Data/Players.csv")
            stats_df.to_csv("./Scrapped_Data/stats.csv")
            nat_stats_df.to_csv("./Scrapped_Data/natstats.csv")
            transfers_df.to_csv("./Scrapped_Data/Transfers.csv")
            break
        del player
    driver.quit()
    print("Finished scrapping")
    players_df.to_csv("./Scrapped_Data/Players.csv")
    stats_df.to_csv("./Scrapped_Data/stats.csv")
    nat_stats_df.to_csv("./Scrapped_Data/natstats.csv")
    transfers_df.to_csv("./Scrapped_Data/Transfers.csv")

info_cols=['Id','tm_Id','Name', 'Team', 'Nationality', 'Date of Birth', 'Height', 'Strong Foot', 'Position', 'Joined', 'Contract Expires', 'Followers']
players_df = hp.create_or_open(file_dest = "./Scrapped_Data/Players.csv", columns = info_cols)

stats_cols = ['Player_Id', 'tm_Id', 'Name', 'Team', 'Season', 'Competition', 'Attribute','value']
stats_df = hp.create_or_open("./Scrapped_Data/Stats.csv", columns = stats_cols)

nat_cols = ["Player_Id", "tm_Id", "Name","National Team","Competition"]
nat_stats_df = hp.create_or_open("./Scrapped_Data/natstats.csv", columns = nat_cols) 

tran_cols=['Player_Id', "tm_Id", 'Name', 'From', 'To', 'Fee', 'Market Value', 'Season', 'Date']
transfers_df = hp.create_or_open("./Scrapped_Data/Transfers.csv", columns = tran_cols)


player_links = pd.read_csv('Prerequisit Data/playerlinks.csv')['Player_url']
transfer_links = pd.read_csv('Prerequisit Data/transferlinks.csv')['Player_url']
team_links = pd.read_csv('Prerequisit Data/teamlinks.csv')['Team_url']


start = 0; end = 3

start_scrapping(driver, start = start, end = end, players_df = players_df, stats_df = stats_df, 
nat_stats_df = nat_stats_df, transfers_df = transfers_df, player_links = player_links, transfer_links = transfer_links)

