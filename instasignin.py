from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.firefox.options import Options
from notify_run import Notify
import numpy as np
import pandas as pd
import time
import csv
import players as pl
import helpers as hp
import sys

# opts = Options()
# opts.headless = False
# driver = webdriver.Firefox(options= opts)


def sign_in(driver):
    driver.get("https://www.instagram.com/")
    username = "grno53"
    password = "grnogrno22"
    time.sleep(10)
    username_field = driver.find_elements_by_css_selector(".zyHYP")[0]
    pass_field = driver.find_elements_by_css_selector(".zyHYP")[1]
    username_field.send_keys(username)
    pass_field.send_keys(password)
    sign_in_button = driver.find_elements_by_css_selector(".y3zKF , .y3zKF ._4EzTm")[0]
    sign_in_button.click()
    time.sleep(10)