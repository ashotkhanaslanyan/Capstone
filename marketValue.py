from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time


driver = webdriver.Firefox()

driver.get("https://www.transfermarkt.com/kylian-mbappe/marktwertverlauf/spieler/342229")

MVCsvHead = pd.DataFrame(columns = ['Name', 'Club', 'Date', 'Age', 'Market Value'])
MVCsvHead.to_csv('markval.csv', mode='a')

name = driver.find_element_by_xpath("//h1")

bgDiv = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'row', ' ' )) and (((count(preceding-sibling::*) + 1) = 16) and parent::*)]")
container = driver.find_element_by_xpath("//*[@id='highcharts-0']").find_element_by_tag_name("svg").find_element_by_class_name("highcharts-series-group").find_elements_by_tag_name("g")[1]
records = container.find_elements_by_tag_name("image")

driver.execute_script("arguments[0].scrollIntoView();", bgDiv)

marketVals = pd.DataFrame(columns = ['Name', 'Club', 'Date', 'Age', 'Market Value'])

for transRecord in records:

	ActionChains(driver).move_to_element(transRecord).perform()
	# ignored_exceptions=StaleElementReferenceException
	# hovInfo = driver.find_element_by_xpath("//*[@id='highcharts-0']").find_element_by_class_name("highcharts-tooltip").find_element_by_xpath("/").find_elements_by_tag_name("b")
	
	# hovInfo = WebDriverWait(driver, 10,ignored_exceptions=ignored_exceptions).until(EC.presence_of_all_elements_located(driver.find_element_by_xpath("//*[@id='highcharts-0']").find_element_by_class_name("highcharts-tooltip").find_element_by_xpath("/").find_elements_by_tag_name("b")))

	# print(hovInfo)
	# marketVals = marketVals.append({'Name': name, 'Club': hovInfo[2].text, 'Date': hovInfo[0].text, 'Age': hovInfo[3].text, 'Market Value': hovInfo[1].text}, ignore_index = True)

# marketVals.to_csv('markvals.csv', mode='a', header=False)
