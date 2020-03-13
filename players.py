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
class Player:
    def __init__(self, id, link, driver):
        blank_info = {
        'Id': "no info",
        'Name': "no_info", 
        'Team': "no_info", 
        'Citizenship:': "no_info", 
        'Date of birth:': "no_info", 
        'Height:': "no_info", 
        'Foot:': "no_info",
        'Position:': "no_info", 
        'Joined:': "no_info", 
        'Contract expires:': "no_info", 
        'Followers': "no_info"
        }
        self.driver = driver
        self.id = id
        self.link = link
        self.info = blank_info
        self.get_info()
        self.get_followers()

    def wait_for_elements(self, xpath):
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        result = ""
        try:
            time.sleep(3)
            result = self.driver.find_elements_by_xpath()
        except:
            result = "no info"
        return result
    

    def get_info(self):
        print("trying to get information about the player")
        info_keys_xpath = "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'auflistung', ' ' ))]//th"
        info_values_xpath = "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'auflistung', ' ' ))]//td"
        team_xpath = "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hauptpunkt', ' ' ))]//*[(@class = 'vereinprofil_tooltip tooltipstered')]"
        name_xpath = "//h1"
        keys = None; values = None; name = None; team = None
        try:
            self.driver.get(self.link)
            keys = self.driver.find_elements_by_xpath(info_keys_xpath)
            values = self.driver.find_elements_by_xpath(info_values_xpath)
            name = self.driver.find_element_by_xpath(name_xpath).text
            team = self.driver.find_element_by_xpath(team_xpath).text
        except NoSuchElementException as exception:
            print("Waiting for the elements")
            print(exception.__str__)
            # time.sleep(3)
            check_value = lambda input: input is None 
            keys = self.wait_for_elements(info_keys_xpath) if check_value(keys) else keys
            values = self.wait_for_elements(info_values_xpath) if check_value(values) else values
            name = self.wait_for_elements(name_xpath) if check_value(name) else name
            team = self.wait_for_elements(team_xpath) if check_value(team) else team

        take_text = lambda input: input.text
        info = dict(zip(map(take_text,keys), map(take_text,values)))
        info.update({
            "Name": name,
            "Team": team,
            "Id": self.id
        })
        self.info.update(info)

    def get_followers(self):
        print("trying to get information about the player's followers")
        insta_xpath = "//*[@title='Instagram']"
        followers_xpath = "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'Y8-fY', ' ' )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'g47SY', ' ' ))]"
        insta_link = None
        try:
            # time.sleep(3)
            insta_link = self.driver.find_element_by_xpath(insta_xpath).get_attribute("href")
            if not(insta_link is None):
                self.driver.get(insta_link)
                followers = self.driver.find_element_by_xpath(followers_xpath).get_attribute("title")
                self.driver.get(self.link)
        except:
            print("no info about followers")
            followers = "no info"

        self.info["Followers"] = followers
    
    def data_to_append(self):
        data = {
            'Id': self.info["Id"],
            'Name':  self.info["Name"], 
            'Team':  self.info["Team"], 
            'Nationality':  self.info["Citizenship:"], 
            'Date of Birth':  self.info["Date of birth:"], 
            'Height':  self.info["Height:"], 
            'Strong Foot':  self.info["Foot:"], 
            'Position':  self.info["Position:"], 
            'Joined':  self.info["Joined:"], 
            'Contract Expires':  self.info["Contract expires:"], 
            'Followers':  self.info["Followers"]
        }
        return data




