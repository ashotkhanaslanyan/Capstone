import pandas as pd
from bs4 import BeautifulSoup
import html5lib
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

def get_trophies(bs_obj, class_, sofifa_id, name):
    try:
        table_html = bs_obj.find('table',class_)
        table = pd.read_html(str(table_html))[0]
        trophies = hp.clean_trophies(table, sofifa_id=sofifa_id, name = name)
        trophies.set_index("sofifa_id", drop = False, inplace = True)
        trophies.to_csv("Scrapped_Data/trophies.csv", mode = 'a', header = False)
    except Exception as e:
        print(str(e))

def get_injuries(bs_obj, class_, sofifa_id, name):
    try:
        table_html = bs_obj.find('table',class_)
        table = pd.read_html(str(table_html))[0]
        injuries = hp.clean_injuries(table, sofifa_id=sofifa_id, name = name)
        injuries.set_index("sofifa_id", drop = False, inplace = True)
        injuries.to_csv("Scrapped_Data/sidelined.csv", mode = 'a', header = False)
    except Exception as e:
        print(str(e))    


def get_injuries_trophies(link, driver, sofifa_id, name):
    try:
        driver.get(link)
        bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
        get_trophies(bs_obj, "real-trophies no-link table-hover table trophies trophies-table", sofifa_id, name)
        get_injuries(bs_obj, "real-sidelined no-link table-hover sidelined table", sofifa_id, name)
    except Exception as e:
        print(str(e))

def start_scrapping(start,end,links,driver):

    dest_cols = {
        "./Scrapped_Data/sidelined.csv" : ["sofifa_id","Name","Reason","Start Date","End Date"],
        "./Scrapped_Data/trophies.csv" : ["sofifa_id","Name","Competition","Trophy","Season"]
    }

    for dest,cols  in dest_cols.items():
        if(not(hp.check_if_exists(dest = dest))):
            hp.create_empty_df(file_dest = dest, columns = cols)

    try:
        for row in range(start,end):
            link = links[row]
            sofifa_id = ids[row]
            name = names[row]
            print("Scrapping trophies,injuries for player with id " + str(sofifa_id))
            get_injuries_trophies(link,driver,sofifa_id,name)
    except Exception as e:
        print(str(e))
    driver.quit()

start_scrapping(start = 93, end = 122, links = links, driver = driver)