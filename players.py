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
import functools
import re
import requests

class Player:
    def __init__(self, id, link, driver, df_path, stats_path, nat_stats_path, transfers_path):
        self.name = "no_info"
        self.driver = driver
        self.id = id
        self.link = link
        self.info_df = None
        self.followers = None
        self.df_path = df_path
        self.stats_path = stats_path
        self.nat_stats_path = nat_stats_path
        self.transfers_path = transfers_path
        self.position = None
        self.tm_Id = None
        print(self.id)
        self.get_tm_id()
        self.get_info()
        self.get_followers()
        self.data_to_append()
        self.get_player_stats()
        self.get_nat_stats()
        self.get_transfers()

    def get_transfers(self):
        print("trying to get player's transfers")
        transfers = pd.DataFrame(columns=['Player_Id', "tm_Id", 'Name', 'From', 'To', 'Fee', 'Market Value', 'Season', 'Date'])
        try:
            link = self.link.replace("profil","transfers")
            self.driver.get(link)
            bs_obj = BeautifulSoup(self.driver.page_source, 'html.parser')
            rows = bs_obj.find_all('table')[0].find('tbody').find_all('tr',{"class":"zeile-transfer"})
            for row in rows:
                cols = row.find_all('td')
                data = {
                    "Player_Id": self.id,
                    "tm_Id": self.tm_Id,
                    "Name": self.name,
                    "From": cols[5].get_text(),
                    "To": cols[9].get_text(),
                    "Fee": cols[11].get_text(),
                    "Market Value": cols[10].get_text(),
                    "Season": cols[0].get_text(),
                    "Date": cols[1].get_text()
                }
                transfers = transfers.append(data, ignore_index=True)
                transfers.set_index("tm_Id", inplace=True, drop=False)
                transfers.to_csv(self.transfers_path, mode = "a", header= False)
        except Exception as e:
            print(str(e))
        # self.transfers_df = transfers

    def go_detailed_page(self):
        detailed = self.driver.find_elements_by_css_selector(".kartei-button-body")[1]
        self.driver.execute_script("arguments[0].click();", detailed)
        time.sleep(5)

    def get_tm_id(self):
        digits = re.findall(r"\d", self.link)
        self.tm_Id = functools.reduce(lambda a,b : a+b,digits)

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
        followers = None
        try:
            insta_link = self.driver.find_element_by_xpath(insta_xpath).get_attribute("href")
            if not(insta_link is None):
                pat = r'.com?\/(.*)/.*'
                username = re.findall(pat, insta_link)[0]
                def_url = "https://www.instagram.com/<username>/?__a=1"
                url = def_url.replace("<username>", username)
                r = requests.get(url = url) 
                data = r.json()
                followers = data["graphql"]["user"]["edge_followed_by"]["count"]
        except Exception as e:
            print("no info about followers, trying to visit the page")
            print(str(e))
            try:
                insta_link = self.driver.find_element_by_xpath(insta_xpath).get_attribute("href")
                if not(insta_link is None):
                    self.driver.get(insta_link)
                    time.sleep(2)
                    bs_obj = BeautifulSoup(self.driver.page_source, 'html.parser')
                    followers = bs_obj.find_all("span", class_="g47SY")[1]["title"]
            except Exception as e:
                print("another exception, catching it")
                print(str(e))
        finally:
            if(followers is None):
                print("nothing found")
                followers = "no info"
            else:
                print("number of followers",followers)
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
        try:
            data = {
                'Id': self.id,
                'tm_Id': self.tm_Id,
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
            df = pd.DataFrame(columns = ['Id','tm_Id','Name', 'Team', 'Nationality', 'Date of Birth', 'Height', 'Strong Foot', 'Position', 'Joined', 'Contract Expires', 'Followers'])
            df = df.append(data, ignore_index = True)
            df.set_index("tm_Id", inplace=True, drop=False)
            df.to_csv(self.df_path, mode = "a", header= False)
            self.position = data["Position"]
            self.data = data
        except Exception as e:
            print(str(e))
        # self.position = data["Position"]
        # self.data = data
        # self.df = df

    def get_player_stats(self):
        print("trying to get the player's statistics")
        df_long = None
        teams_xpath = "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' ))]//img"
        # position_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "dataValue", " " ))]'
        try:
            stats_link = self.link.replace("profil","leistungsdatendetails")
            self.driver.get(stats_link)
            self.go_detailed_page()
            get_name = lambda input: input.get_attribute('alt')
            teams = self.driver.find_elements_by_xpath(teams_xpath)
            teams = list(map(get_name, teams))
            bs_obj = BeautifulSoup(self.driver.page_source, 'html.parser')
            table = bs_obj.find_all('table')[1]
            df = pd.read_html(str(table))[0]
            position = self.extract_cell("Position:")
            if(position == "Goalkeeper"):
                columns = ["Season","Team","Competition","Squad",
                    "Appearances","PPG","Goals","Own goals","Substitutions on",
                    "Substitutions off","Yellow Cards","Second yellow cards","Red cards",
                    "Goals conceded","Clean sheets","Minutes played"]
                drop_indexes = [3,17]
                drop_cols = ["Goals"]
            else:
                columns = ["Season","Team","Competition","Squad",
                "Appearances","PPG","Goals","Assists","Own goals","Substitutions on",
                "Substitutions off","Yellow Cards","Second yellow cards","Red cards",
                "Penalty goals","Minutes per goal","Minutes played"]
                drop_indexes = [3,18]
                drop_cols = []
            id_vars = ["Player_Id","tm_Id","Name","Team","Season","Competition"]
            df_long = hp.clean_stats_frame(df = df, teams = teams, team_ind = 1, player_id = self.id,
            player_name = self.name, columns = columns, drop_indexes = drop_indexes,
            drop_cols = drop_cols, id_vars = id_vars, tm_id = self.tm_Id)
            df_long.set_index("tm_Id", inplace=True, drop=False)
            df_long.to_csv(self.stats_path, mode = "a", header= False)
        except Exception as e:
            print(str(e))

    def get_nat_stats(self):
        print("trying to get the player's national team statistics")
        nat_team_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "tooltipstered", " " ))]'
        df_long = None
        try:
            nat_link = self.link.replace("profil","nationalmannschaft")
            self.driver.get(nat_link)
            self.go_detailed_page()
            nat_team = self.driver.find_element_by_xpath(nat_team_xpath).text
            bs_obj = BeautifulSoup(self.driver.page_source, 'html.parser')
            table = bs_obj.find_all('table')[2]
            df = pd.read_html(str(table))[0]
            position = self.extract_cell("Position:")
            if(position == "Goalkeeper"):
                columns = ["National Team","Competition",
                        "Appearances","Goals","Own goals","Substitutions on",
                        "Substitutions off","Yellow Cards","Second yellow cards","Red cards",
                        "Goals conceded","Clean sheets","Minutes played"]
                drop_indexes = [13]
                drop_cols = ["Goals"]
            else:
                drop_indexes = [14]
                columns = ["National Team","Competition","Squad",
                        "Goals","Assists","Own goals","Substitutions on",
                        "Substitutions off","Yellow Cards","Second yellow cards","Red cards",
                        "Penalty goals","Minutes per goal","Minutes played"]
                drop_cols = []
            id_vars = ["Player_Id","tm_Id","Name","National Team","Competition"]
            df_long = hp.clean_stats_frame(df = df, teams = nat_team, team_ind = 0, player_id = self.id,
            player_name = self.name, columns = columns, drop_indexes = drop_indexes,
            drop_cols = drop_cols, id_vars = id_vars, tm_id = self.tm_Id)
            df_long.set_index("tm_Id", inplace=True, drop=False)
            df_long.to_csv(self.nat_stats_path, mode = "a", header= False)
        except Exception as e:
            print(str(e))
