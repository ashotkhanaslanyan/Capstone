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

link =  "https://www.instagram.com/sah.narek/?__a=1"
r = requests.get(url = link) 
data = r.json() 
print(data["graphql"]["user"]["edge_followed_by"]["count"])
# opts = Options()
# opts.headless = False
# driver = webdriver.Firefox(options= opts)

# driver.get("https://www.instagram.com/n.suele/")

# # bs_obj = BeautifulSoup(driver.page_source, 'html.parser')
# # followers = bs_obj.find_all("span", class_="g47SY")[1]["title"]
# print(followers)
# driver.quit()