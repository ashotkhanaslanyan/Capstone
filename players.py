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
from bs4 import BeautifulSoup
import time
import helpers as hp

class Player:
    def __init__(self, id, link, driver):
        self.name = "no_info"
        self.driver = driver
        self.id = id
        self.link = link
        self.info_df = None
        self.followers = None
        self.stats_df = None
        self.nat_stats = None
        self.position = None
        self.get_info()
        self.get_followers()
        self.data_to_append()
        self.get_player_stats()
        self.get_nat_stats()

    def get_info(self):
        print("trying to get information about the player")
        try:
            self.driver.get(self.link)
            bs_obj = BeautifulSoup(self.driver.page_source, 'html.parser')
            name = bs_obj.find_all('h1')[0].get_text()
            table = bs_obj.find_all('table')[0]
            df = pd.read_html(str(table))[0]
            df.columns = ["Key", "Value"]
            self.info_df = df
            self.name = name
        except Exception as e:
            print(str(e))

    def get_followers(self):
        print("trying to get information about the player's followers")
        insta_xpath = "//*[@title='Instagram']"
        insta_link = None
        try:
            insta_link = self.driver.find_element_by_xpath(insta_xpath).get_attribute("href")
            if not(insta_link is None):
                self.driver.get(insta_link)
                bs_obj = BeautifulSoup(self.driver.page_source, 'html.parser')
                followers = bs_obj.find_all("span", class_="g47SY")[1]["title"]
        except Exception as e:
            print("no info about followers")
            print(str(e))
            followers = "no info"

        self.followers = followers
    
    def extract_cell(self, key):
        result = None
        df = self.info_df
        try:
            result = df[df["Key"] == key]["Value"].values[0]
        except:
            print("the player does not have " + str(key))
            result = "no_info"
        return result

    def data_to_append(self):
        data = {
            'Id': self.id,
            'Name':  self.name, 
            'Team':  self.extract_cell("Current club:"), 
            'Nationality':  self.extract_cell("Citizenship:"), 
            'Date of Birth':  self.extract_cell("Date of birth:"), 
            'Height':  self.extract_cell("Height:"), 
            'Strong Foot':  self.extract_cell("Foot:"), 
            'Position':  self.extract_cell("Position:"), 
            'Joined':  self.extract_cell("Joined:"), 
            'Contract Expires':  self.extract_cell("Contract expires:"), 
            'Followers':  self.followers
        }
        self.position = data["Position"]
        self.data = data

    def get_player_stats(self):
        print("trying to get the player's statistics")
        df_long = None
        teams_xpath = "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' ))]//img"
        # position_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "dataValue", " " ))]'
        try:
            stats_link = self.link.replace("profil","leistungsdatendetails")
            self.driver.get(stats_link)
            detailed = self.driver.find_elements_by_css_selector(".kartei-button-body")[1]
            self.driver.execute_script("arguments[0].click();", detailed)
            time.sleep(3)
            get_name = lambda input: input.get_attribute('alt')
            teams = self.driver.find_elements_by_xpath(teams_xpath)
            teams = list(map(get_name, teams))
            bs_obj = BeautifulSoup(self.driver.page_source, 'html.parser')
            table = bs_obj.find_all('table')[1]
            df = pd.read_html(str(table))[0]
            position = self.position
            if(position == "Goalkeeper"):
                columns = ["Season","Team","Competition","Squad",
                    "Appearances","PPG","Goals","Own goals","Substitutions on",
                    "Substitutions off","Yellow Cards","Second yellow cards","Red cards",
                    "Goals conceded","Clean sheets","Minutes played"]
                drop_indexes = [3,17]
            else:
                columns = ["Season","Team","Competition","Squad",
                "Appearances","PPG","Goals","Assists","Own goals","Substitutions on",
                "Substitutions off","Yellow Cards","Second yellow cards","Red cards",
                "Penalty goals","Minutes per goal","Minutes played"]
                drop_indexes = [3,18]
            id_vars = ["Player_Id","Name","Team","Season","Competition"]
            df_long = hp.hp.clean_stats_frame(df = df, teams = teams, player_id = self.id,
            player_name = self.name, columns = columns, drop_indexes = drop_indexes, id_vars = id_vars)
        except Exception as e:
            print(str(e))
        self.stats_df = df_long

    def get_nat_stats(self):
        print("trying to get the player's national team statistics")
        nat_team_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "tooltipstered", " " ))]'
        df_long = None
        try:
            nat_link = self.link.replace("profil","nationalmannschaft")
            self.driver.get(nat_link)
            detailed = self.driver.find_elements_by_css_selector(".kartei-button-body")[1]
            self.driver.execute_script("arguments[0].click();", detailed)
            time.sleep(3)
            nat_team = self.driver.find_element_by_xpath(nat_team_xpath).text
            bs_obj = BeautifulSoup(self.driver.page_source, 'html.parser')
            table = bs_obj.find_all('table')[2]
            df = pd.read_html(str(table))[0]
            position = self.position
            if(position == "Goalkeeper"):
                columns = ["National Team","Competition",
                        "Appearances","Goals","Own goals","Substitutions on",
                        "Substitutions off","Yellow Cards","Second yellow cards","Red cards",
                        "Goals conceded","Clean sheets","Minutes played"]
                drop_indexes = [13]
            else:
                drop_indexes = [14]
                columns = ["National Team","Competition","Squad",
                        "Goals","Assists","Own goals","Substitutions on",
                        "Substitutions off","Yellow Cards","Second yellow cards","Red cards",
                        "Penalty goals","Minutes per goal","Minutes played"]

            id_vars = ["Player_Id","Name","National Team","Competition"]
            df_long = hp.clean_stats_frame(df = df, teams = nat_team, player_id = self.id,
            player_name = self.name, columns = columns, drop_indexes = drop_indexes, id_vars = id_vars)
        except Exception as e:
            print(str(e))
        self.nat_stats = df_long

