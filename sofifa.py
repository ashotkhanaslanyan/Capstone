import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import helpers as hp

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)

players_20 = pd.read_csv("fifa-20-complete-player-dataset/real_life.csv")
links = players_20["player_url"]
ids = players_20["sofifa_id"]
names = players_20["short_name"]

def get_injuries_trophies(link, driver, sofifa_id, name):
    try:
        driver.get(link)
        bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
        table = bs_obj.find_all('table')[1]
        table_1 = bs_obj.find_all('table')[2]
        trophy_df = pd.read_html(str(table))[0]
        injury_df = pd.read_html(str(table_1))[0]
        trophies = hp.clean_trophies(trophy_df, sofifa_id=sofifa_id, name = name)
        injuries = hp.clean_injuries(injury_df, sofifa_id=sofifa_id, name = name)
    except Exception as e:
        print(str(e))
    return  injuries,trophies

def start_scrapping(start,end,links,driver):
    inj_cols = ["sofifa_id","Name","Reason","Start Date","End Date"]
    injuries_df = hp.create_or_open("./Scrapped_Data/sidelined.csv", columns = inj_cols)
    tr_cols = ["sofifa_id","Name","Competition","Trophy","Season"]
    trophies_df = hp.create_or_open("./Scrapped_Data/trophies.csv", columns =tr_cols)
    try:
        for row in range(start,end):
            link = links[row]
            sofifa_id = ids[row]
            name = names[row]
            print("Scrapping trophies,injuries for player with id " + str(sofifa_id))
            injury_df,trophy_df = get_injuries_trophies(link,driver,sofifa_id,name)
            injuries_df = injuries_df.append(injury_df)
            trophies_df = trophies_df.append(trophy_df)
    except Exception as e:
        print(str(e))
        print("exception !!!, writting to csv injuries stopped_at", str(injuries_df.tail[1]["sofifa_id"]))
        print("exception !!!, writting to csv trophies stopped_at", str(trophies_df.tail[1]["sofifa_id"]))
        injuries_df.to_csv("./Scrapped_Data/sidelined.csv")
        trophies_df.to_csv("./Scrapped_Data/trophies.csv")
    injuries_df.to_csv("./Scrapped_Data/sidelined.csv")
    trophies_df.to_csv("./Scrapped_Data/trophies.csv")
    driver.quit()

start_scrapping(start = 20, end = 30, links = links, driver = driver)