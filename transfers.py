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
driver = webdriver.Firefox(options= opts)

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


def get_transfers(link, id, driver):
    try:
        driver.get(link)
        bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
        rows = bs_obj.find_all('table')[0].find('tbody').find_all('tr',{"class":"zeile-transfer"})
        name = bs_obj.find_all('h1')[0].get_text()
        for row in rows:
            cols = row.find_all('td')
            data = {
                "Player_Id": id,
                "Name": name,
                "From": cols[5].get_text(),
                "To": cols[9].get_text(),
                "Fee": cols[11].get_text(),
                "Market Value": cols[10].get_text(),
                "Season": cols[0].get_text(),
                "Date": cols[1].get_text()
            }
            print('data', data)
            global transfers
            transfers = transfers.append(data, ignore_index=True)
    except Exception as e:
        print(str(e))



for row in range(485, 496):
    try:
        link = transfers_links_data['Player_url'][row]
        get_transfers(link = link, id = row, driver = driver)
    except Exception as e:
        print("exception !!! writting to csv stopped at " +  str(transfers.tail(1)["Player_Id"]))
        print("The exception message", str(e))
        transfers.to_csv("./Scrapped_Data/Transfers.csv")
        break

transfers.to_csv("./Scrapped_Data/Transfers.csv")
driver.quit()