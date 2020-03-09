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

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.headless = True
driver = webdriver.Chrome(chrome_options=chrome_options)

class Player:
    def __init__(self, id, link):
        self.id = id
        self.link = link
        self.get_info()
        self.get_followers()
    
    def get_info(self):
        print("trying to get information about the player")
        info_keys_xpath = "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'auflistung', ' ' ))]//th"
        info_values_xpath = "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'auflistung', ' ' ))]//td"
        team_xpath = "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hauptpunkt', ' ' ))]//*[(@class = 'vereinprofil_tooltip tooltipstered')]"
        name_xpath = "//h1"
        timeout = 3
        info = {}
        try:
            driver.get(self.link)
            keys_present = EC.presence_of_element_located((By.XPATH, info_keys_xpath))
            values_present = EC.presence_of_element_located((By.XPATH, info_values_xpath))
            WebDriverWait(driver, timeout).until(keys_present)
            WebDriverWait(driver, timeout).until(values_present)
            keys = driver.find_elements_by_xpath(info_keys_xpath)
            values = driver.find_elements_by_xpath(info_values_xpath)
            name = driver.find_element_by_xpath(name_xpath).text
            team = driver.find_element_by_xpath(team_xpath).text
            take_text = lambda input: input.text
            info = dict(zip(map(take_text,keys), map(take_text,values)))
            info.update({
                "Name": name,
                "Team": team,
                "ID": self.id
            })
        except:
            print("Something went wrong")
        self.info = info

    def get_followers(self):
        print("trying to get information about the player's followers")
        insta_xpath = "//*[@title='Instagram']"
        followers_xpath = "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'Y8-fY', ' ' )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'g47SY', ' ' ))]"
        timeout = 5
        try:
            insta_link = driver.find_element_by_xpath(insta_xpath).get_attribute("href")
            driver.get(insta_link)
            followers_present = EC.presence_of_element_located((By.XPATH, followers_xpath))
            WebDriverWait(driver, timeout).until(followers_present)
            followers = driver.find_element_by_xpath(followers_xpath).text
            print(followers)
        except:
            print("no info about followers")
            followers = "no info"
        self.info.update({
            "Followers":followers
        })
sven = Player(33,"https://www.transfermarkt.com/manuel-neuer/profil/spieler/17259")
print(sven.info)
