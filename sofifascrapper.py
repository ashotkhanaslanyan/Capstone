from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.firefox.options import Options
import time

numStopped = 1486

sofifaData = pd.read_csv('fifa-20-complete-player-dataset/players_20.csv')

# trophiesHead = pd.DataFrame(columns = ['Name', 'Competitiion', 'Trophie', 'Season'])
# trophiesHead.to_csv('trophies.csv', mode='a')

# sidelinedHead = pd.DataFrame(columns = ['Name', 'Reason', 'Start Date', 'End Date'])
# sidelinedHead.to_csv('sidelined.csv', mode='a')

for row in range(numStopped - 2, len(sofifaData['sofifa_id'])):

	opts = Options()
	opts.headless = True

	driver = webdriver.Firefox(options=opts)
	
	link = sofifaData['player_url'][row]

	driver.get(link[:-9] + 'live')
	# driver.maximize_window()

	# time.sleep(5)

	try:

		name = sofifaData['short_name'][row]
		competCol = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'trophies-table', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'competition', ' ' ))]")
		trophieColPath = "//*[@class = 'real-trophies no-link table-hover table trophies trophies-table']/tbody/tr["
		trophieCountCol = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'trophies-table', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'total', ' ' ))]")
		seasonCol = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'unavailable', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'seasons', ' ' ))]//a")
		ReasonCol = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'sidelined', ' ' ))]//td[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]")
		sdCol = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'startdate', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'timestamp', ' ' ))]")
		edCol = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'odd', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'enddate', ' ' ))]")

		i = 2
		seasonNum = 0

		trophiesCsv = pd.DataFrame(columns = ['Name', 'Competitiion', 'Trophie', 'Season'])

		for ind in range(len(competCol)):
			if (competCol[ind].text == ''):
				competition = competCol[ind - 1].text
			else:
				competition = competCol[ind].text
			try:
				driver.find_element_by_xpath(trophieColPath + str(ind + i) + ']/td[2]')
			except NoSuchElementException:
				i += 1
				try:
					trophie = driver.find_element_by_xpath(trophieColPath + str(ind + i) + ']/td[2]').text
				except NoSuchElementException:
					i += 1
			trophie = driver.find_element_by_xpath(trophieColPath + str(ind + i) + ']/td[2]').text
			numOfTrophies = int(trophieCountCol[ind].text[:-1])
			for j in range(numOfTrophies):
				season = seasonCol[seasonNum].get_attribute('innerHTML')
				seasonNum += 1

				trophiesCsv = trophiesCsv.append({'Name': name, 'Competitiion': competition, 'Trophie': trophie, 'Season': season},ignore_index=True)

		trophiesCsv.to_csv('trophies.csv', mode='a', header=False)

		sidelinedCsv = pd.DataFrame(columns = ['Name', 'Reason', 'Start Date', 'End Date'])

		for ind in range(len(ReasonCol)):
			if(edCol[ind].text == ''):
				ed = '-'
			else:
				ed = edCol[ind].text
			sidelinedCsv = sidelinedCsv.append({'Name': name, 'Reason': ReasonCol[ind].text, 'Start Date': sdCol[ind].text, 'End Date': ed}, ignore_index=True)

		sidelinedCsv.to_csv('sidelined.csv', mode='a', header=False)

		driver.quit()

	except WebDriverException:

		driver.quit()