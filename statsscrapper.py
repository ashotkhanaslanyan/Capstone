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

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)

def create_or_open(file_dest, columns):
    data_frame = None
    try:
        data_frame = pd.read_csv(file_dest, index_col = 0)
    except:
        data_frame = pd.DataFrame(columns=columns)
    return data_frame

columns=['Player_Id', 'Name', 'From', 'To', 'Fee', 'Market Value', 'Season', 'Date']
transfers = create_or_open("./Scrapped_Data/Transfers.csv", columns)
transfers_links_data = pd.read_csv('Prerequisit Data/transferlinks.csv')

def clean_stats_frame(df,teams,player_id,player_name, columns): 
    df.drop(df.tail(1).index,inplace=True)
    df.iloc[:,1] = teams
    df = df.drop(df.columns[[3,18]], axis = 1)
    df.columns = columns
    df.insert(0,"Player_Id", player_id)
    df.insert(1,"Name", player_name)
    df["PPG"] = df["PPG"] / 100
    df_long = pd.melt(df, id_vars = ["Player_Id","Name","Team","Season","Competition"], var_name = "Attribute")
    return df_long


def get_player_stats(link, player_id, driver, columns):    
    driver.get(link)
    detailed = driver.find_elements_by_css_selector(".kartei-button-body")[1]
    driver.execute_script("arguments[0].click();", detailed)
    time.sleep(3)
    get_name = lambda input: input.get_attribute('alt')
    teams = driver.find_elements_by_css_selector(".tiny_wappen")
    teams = list(map(get_name, teams))
    bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
    name = bs_obj.find_all('h1')[0].get_text()
    table = bs_obj.find_all('table')[1]
    df = pd.read_html(str(table))[0]
    df_long = clean_stats_frame(df = df, teams = teams, player_id = player_id, player_name = name, columns = columns)
    df_long.to_csv("./Scrapped_Data/Stats_Long.csv")

link = "https://www.transfermarkt.com/cristiano-ronaldo/leistungsdatendetails/spieler/8198"
columns = ["Season","Team","Competition","Squad",
"Appearances","PPG","Goals","Assists","Own goals","Substitutions on",
"Substitutions off","Yellow Cards","Second yellow cards","Red cards",
"Penalty goals","Minutes per goal","Minutes played"]
get_player_stats(link = link, player_id = 7, driver = driver, columns = columns)
driver.quit()

transfers.to_csv("./Scrapped_Data/Transfers.csv")
driver.quit()