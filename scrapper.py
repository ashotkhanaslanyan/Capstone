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

playersCsvHead = pd.DataFrame(columns=['Id','Name', 'Team', 'Nationality', 'Date of Birth', 'Height', 'Strong Foot', 'Position', 'Joined', 'Contract Expires', 'Followers'])
playersCsvHead.to_csv('./Scrapped_Data/Players.csv', mode='a')

transfersCsvHead = pd.DataFrame(columns=['Player_Id','Name', 'From', 'To', 'Fee', 'Market Value', 'Season', 'Date'])
transfersCsvHead.to_csv('./Scrapped_Data/Transfers.csv', mode='a')

StatsCsvHead = pd.DataFrame(columns=['Player_Id','Name', 'Position', 'Team', 'Season', 'Competition', 'Attribute', 'Value'])
StatsCsvHead.to_csv('./Scrapped_Data/stats.csv', mode='a')

NatCsvHead = pd.DataFrame(columns = ['Player_Id','Name', 'Position', 'Competition', 'Attribute', 'Value'])
NatCsvHead.to_csv('./Scrapped_Data/natstats.csv', mode='a')

opts = Options()
opts.headless = True

driver = webdriver.Firefox(options= opts)

driver.get("https://www.transfermarkt.com/1-bundesliga/startseite/wettbewerb/L1")

allTeams = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hide-for-pad', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'tooltipstered', ' ' ))]")

teamLinks = pd.read_csv('Prerequisit Data/teamlinks.csv')
playerLinksData = pd.read_csv('Prerequisit Data/playerlinks.csv')

def PlayerPage(link, playerId):
	
	playersData = pd.DataFrame(columns=['Id', 'Name', 'Team', 'Nationality', 'Date of Birth', 'Height', 'Strong Foot', 'Position', 'Joined', 'Contract Expires', 'Followers'])
	transfersData = pd.DataFrame(columns=['Player_Id', 'Name', 'From', 'To', 'Fee', 'Market Value', 'Season', 'Date'])

	driver.get(link)

	time.sleep(10)
	
	infoTags = [driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'auflistung', ' ' ))]//th"), driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'auflistung', ' ' ))]//td")]

	def getNat():
		
		infoTags

		for key in infoTags[0]:
			if(key.text == 'Citizenship:'):
				ind = infoTags[0].index(key)
				return infoTags[1][ind]

	def getFoot():

		infoTags

		for key in infoTags[0]:
			if(key.text == 'Foot:'):
				ind = infoTags[0].index(key)
				return infoTags[1][ind]

	def getFollowers(pageLink):

		driver.get(pageLink)
		return driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'Y8-fY', ' ' )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'g47SY', ' ' ))]")

	name = driver.find_element_by_xpath("//h1").text
	team = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hauptpunkt', ' ' ))]//*[(@class = 'vereinprofil_tooltip tooltipstered')]").text
	dob = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataDaten', ' ' )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]//p[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataValue', ' ' ))]").text
	hgt = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataDaten', ' ' )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//p[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataValue', ' ' ))]").text
	pos = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataDaten', ' ' )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//p[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataValue', ' ' ))]").text
	joined = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataValue', ' ' )) and (((count(preceding-sibling::*) + 1) = 9) and parent::*)]").text
	until = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataValue', ' ' )) and (((count(preceding-sibling::*) + 1) = 12) and parent::*)]").text
	nat = getNat().text
	
	try:
		foot = getFoot().text
	except:
		foot = 'none'

	driver.find_element_by_xpath("//*[@id = 'transfers']").click()
	time.sleep(3)

	numOfTransfers = len(driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zeile-transfer', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hide-for-small', ' ' )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]"))

	transferSeasons = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zeile-transfer', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hide-for-small', ' ' )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]")
	transferDates = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zeile-transfer', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' ))]")
	del transferDates[::3]
	del transferDates[1::2]
	teamLeft = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'vereinsname', ' ' )) and (((count(preceding-sibling::*) + 1) = 6) and parent::*)]//a")
	teamJoined = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'vereinsname', ' ' )) and (((count(preceding-sibling::*) + 1) = 10) and parent::*)]//a")
	markVals = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zeile-transfer', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zelle-mw', ' ' ))]")
	fees = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zeile-transfer', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zelle-abloese', ' ' ))]")

	for i in range(numOfTransfers):

		transfersData = transfersData.append({'Player_Id': playerId, 'Name': name, 'From': teamLeft[i].text, 'To': teamJoined[i].text, 'Fee': fees[i].text, 'Market Value': markVals[i].text, 'Season': transferSeasons[i].text, 'Date': transferDates[i].text}, ignore_index=True)
	
	transfersData.to_csv('./Scrapped_Data/Transfers.csv', mode='a', header=False)

	driver.find_element_by_xpath("//*[(@id = 'profile')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'megamenu', ' ' ))]").click()

	time.sleep(3)

	try:
		driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'leistungsdatenContent', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'swiper-slide-active', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'button', ' ' ))]").click()
	except:
		print("the element was not found, trying another way")
		newLink = link.replace("profil","leistungsdatendetails")
		driver.get(newLink)		
	
	time.sleep(2)

	# filtersDiv = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'large-8', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'content', ' ' ))]")
	filters = driver.find_elements_by_tag_name('select')
	filters = filters[4:]

	for fltr in filters:
		fltrParent = fltr.find_element_by_xpath('..')
		fltrParent.click()
		inputFiltr = fltrParent.find_element_by_tag_name('input')
		inputFiltr.send_keys('all')
		inputFiltr.send_keys(Keys.ENTER)



	driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'button', ' ' ))]").click()
	time.sleep(5)
	driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'kartei-number-2', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'kartei-button-body', ' ' ))]").click()

	time.sleep(3)

	def getGkInternStats(playerId):
		
		statsData = pd.DataFrame(columns=['Player_Id','Name', 'Position', 'Team', 'Season', 'Competition', 'Attribute', 'Value'])

		attributes = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-minuten-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-ohnegegentor-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-gegentor-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-rotekarte-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-gelbrotekarte-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-gelbekarte-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-auswechslungen-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-einwechslungen-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-eigentor-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-tor-table-header', ' ' ))] | //*[(@id = 'yw1_c6')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'sort-link', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-einsaetze-table-header', ' ' ))] | //*[(@id = 'yw1_c4')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'sort-link', ' ' ))]")
		competitions = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'no-border-links', ' ' ))]//a")
		staSeasons = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]")
		teamStats = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' ))]//img")
		wasInSquad = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 5) and parent::*)]")
		appearancesStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 6) and parent::*)]")
		ppgStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 7) and parent::*)]")
		goalsStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 8) and parent::*)]")
		ownGoalsStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 9) and parent::*)]")
		subOnStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 10) and parent::*)]")
		subOffStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 11) and parent::*)]")
		yellowStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 12) and parent::*)]")
		yellowRedStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 13) and parent::*)]")
		redStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 14) and parent::*)]")
		goalsConseadedStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 15) and parent::*)]")
		cleanSheetStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 16) and parent::*)]")
		minutesPlayedStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'rechts', ' ' ))]")

		def GetValueOfAttribute(att):
			if(att.get_attribute('title') == 'Appearances'):
				return appearancesStats
			elif(att.get_attribute('title') == 'Goals'):
				return goalsStats
			elif(att.get_attribute('title') == 'Points per match'):
				return ppgStats
			elif(att.get_attribute('title') == 'Own goals'):
				return ownGoalsStats
			elif(att.get_attribute('title') == 'Substitutions on'):
				return subOnStats
			elif(att.get_attribute('title') == 'Substitutions off'):
				return subOffStats
			elif(att.get_attribute('title') == 'Yellow cards'):
				return yellowStats
			elif(att.get_attribute('title') == 'Second yellow cards'):
				return yellowRedStats
			elif(att.get_attribute('title') == 'Red cards'):
				return redStats
			elif(att.get_attribute('title') == 'Goals conceded'):
				return goalsConseadedStats
			elif(att.get_attribute('title') == 'Clean sheets'):
				return cleanSheetStats
			elif(att.get_attribute('title') == 'Minutes played'):
				return minutesPlayedStats
			elif(att.text == 'Squad'):
				return wasInSquad

		for attribute in attributes:

			value = GetValueOfAttribute(attribute)
			att = attribute.get_attribute('title')
			if(att == ''):
				att = attribute.text
			for i in range(len(staSeasons)):

				teamToApp = teamStats[i].get_attribute('alt')
				seasonToApp = staSeasons[i].text
				compToApp = competitions[i].text
				try:
					valToApp = value[i].text
				except TypeError:
					valToApp = '-'
				statsData = statsData.append({'Player_Id': playerId, 'Name': name, 'Position': pos, 'Team': teamToApp, 'Season': seasonToApp, 'Competition': compToApp, 'Attribute': att, 'Value': valToApp}, ignore_index=True)

		statsData.to_csv('./Scrapped_Data/stats.csv',mode='a', header = False)
		driver.find_element_by_xpath("//*[(@id = 'profile')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'megamenu', ' ' ))]").click()

	def getGkNatStats(playerId):

		statsData = pd.DataFrame(columns=['Player_Id', 'Name', 'Position', 'Competition', 'Attribute', 'Value'])

		attributes = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icons_sprite', ' ' ))]")
		competitions = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'no-border-links', ' ' ))]//a")
		appearancesStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 3) and parent::*)]")
		goalsStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 4) and parent::*)]")
		ownGoalsStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 5) and parent::*)]")
		subOnStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 6) and parent::*)]")
		subOffStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 7) and parent::*)]")
		yellowStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 8) and parent::*)]")
		yellowRedStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 9) and parent::*)]")
		redStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 10) and parent::*)]")
		goalsConseadedStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 11) and parent::*)]")
		cleanSheetStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 12) and parent::*)]")
		minutesPlayedStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'rechts', ' ' ))]")

		def GetValueOfAttribute(att):
			if(att.get_attribute('title') == 'Appearances'):
				return appearancesStats
			elif(att.get_attribute('title') == 'Goals'):
				return goalsStats
			elif(att.get_attribute('title') == 'Own goals'):
				return ownGoalsStats
			elif(att.get_attribute('title') == 'Substitutions on'):
				return subOnStats
			elif(att.get_attribute('title') == 'Substitutions off'):
				return subOffStats
			elif(att.get_attribute('title') == 'Yellow cards'):
				return yellowStats
			elif(att.get_attribute('title') == 'Second yellow cards'):
				return yellowRedStats
			elif(att.get_attribute('title') == 'Red cards'):
				return redStats
			elif(att.get_attribute('title') == 'Goals conceded'):
				return goalsConseadedStats
			elif(att.get_attribute('title') == 'Clean sheets'):
				return cleanSheetStats
			elif(att.get_attribute('title') == 'Minutes played'):
				return minutesPlayedStats

		for attribute in attributes:

			value = GetValueOfAttribute(attribute)
			att = attribute.get_attribute('title')
			for i in range(len(competitions)):
				compToApp = competitions[i].text
				try:
					valToApp = value[i].text
				except TypeError:
					valToApp = '-'
				statsData = statsData.append({'Player_Id': playerId, 'Name': name, 'Position': pos, 'Competition': compToApp, 'Attribute': att, 'Value': valToApp}, ignore_index=True)

		driver.find_element_by_xpath("//*[(@id = 'profile')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'megamenu', ' ' ))]").click()
		statsData.to_csv('./Scrapped_Data/natstats.csv', mode='a', header=False)

	def getInternStats(playerId):

		statsData = pd.DataFrame(columns=['Player_Id', 'Name', 'Position', 'Team', 'Season', 'Competition', 'Attribute', 'Value'])

		attributes = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-minuten-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-minutenprotor-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-elfmeter-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-rotekarte-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-gelbrotekarte-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-gelbekarte-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-auswechslungen-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-einwechslungen-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-eigentor-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-einsaetze-table-header', ' ' ))] | //*[(@id = 'yw1_c4')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'sort-link', ' ' ))] | //*[(@id = 'yw1_c6')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'sort-link', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-vorlage-table-header', ' ' ))] | //*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icon-tor-table-header', ' ' ))]")
		competitions = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'no-border-links', ' ' ))]//a")
		staSeasons = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]")
		teamStats = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' ))]//img")
		wasInSquad = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 5) and parent::*)]")
		appearancesStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 6) and parent::*)]")
		ppgStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 7) and parent::*)]")
		goalsStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 8) and parent::*)]")
		assistStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 9) and parent::*)]")
		ownGoalsStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 10) and parent::*)]")
		subOnStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 11) and parent::*)]")
		subOffStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 12) and parent::*)]")
		yellowStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 13) and parent::*)]")
		yellowRedStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 14) and parent::*)]")
		redStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 15) and parent::*)]")
		penaltyGoalsStats = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 16) and parent::*)]")
		lastCols = driver.find_elements_by_xpath("//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'rechts', ' ' ))]")
		mpgStats = lastCols[::2]
		minutesPlayedStats = lastCols[1::2]

		def GetValueOfAttribute(att):
			if(att.get_attribute('title') == 'Appearances'):
				return appearancesStats
			elif(att.get_attribute('title') == 'Goals'):
				return goalsStats
			elif(att.get_attribute('title') == 'Points per match'):
				return ppgStats
			elif(att.get_attribute('title') == 'Own goals'):
				return ownGoalsStats
			elif(att.get_attribute('title') == 'Substitutions on'):
				return subOnStats
			elif(att.get_attribute('title') == 'Assists'):
				return assistStats
			elif(att.get_attribute('title') == 'Penalty goals'):
				return penaltyGoalsStats
			elif(att.get_attribute('title') == 'Minutes per goal'):
				return mpgStats
			elif(att.get_attribute('title') == 'Substitutions off'):
				return subOffStats
			elif(att.get_attribute('title') == 'Yellow cards'):
				return yellowStats
			elif(att.get_attribute('title') == 'Second yellow cards'):
				return yellowRedStats
			elif(att.get_attribute('title') == 'Red cards'):
				return redStats
			elif(att.get_attribute('title') == 'Minutes played'):
				return minutesPlayedStats
			elif(att.text == 'Squad'):
				return wasInSquad

		for attribute in attributes:

			value = GetValueOfAttribute(attribute)
			att = attribute.get_attribute('title')
			if(att == ''):
				att = attribute.text
			for i in range(len(staSeasons)):
				teamToApp = teamStats[i].get_attribute('alt')
				seasonToApp = staSeasons[i].text
				compToApp = competitions[i].text
				try:
					valToApp = value[i].text
				except TypeError:
					valToApp = '-'
				statsData = statsData.append({'Player_Id': playerId, 'Name': name, 'Position': pos, 'Team': teamToApp, 'Season': seasonToApp, 'Competition': compToApp, 'Attribute': att, 'Value': valToApp}, ignore_index=True)

		statsData.to_csv('./Scrapped_Data/stats.csv', mode='a', header=False)

	def getNatStats(playerId):

		statsData = pd.DataFrame(columns=['Player_Id','Name', 'Position', 'Competition', 'Attribute', 'Value'])

		attributes = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'icons_sprite', ' ' ))]")
		competitions = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'no-border-links', ' ' ))]//a")
		appearancesStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 3) and parent::*)]")
		goalsStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 4) and parent::*)]")
		assistStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 5) and parent::*)]")
		ownGoalsStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 6) and parent::*)]")
		subOnStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 7) and parent::*)]")
		subOffStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 8) and parent::*)]")
		yellowStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 9) and parent::*)]")
		yellowRedStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 10) and parent::*)]")
		redStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 11) and parent::*)]")
		penaltyGoalsStats = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' )) and (((count(preceding-sibling::*) + 1) = 12) and parent::*)]")
		lastCols = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//tbody//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'rechts', ' ' ))]")
		mpgStats = lastCols[::2]
		minutesPlayedStats = lastCols[1::2]

		def GetValueOfAttribute(att):
			if(att.get_attribute('title') == 'Appearances'):
				return appearancesStats
			elif(att.get_attribute('title') == 'Goals'):
				return goalsStats
			elif(att.get_attribute('title') == 'Own goals'):
				return ownGoalsStats
			elif(att.get_attribute('title') == 'Substitutions on'):
				return subOnStats
			elif(att.get_attribute('title') == 'Substitutions off'):
				return subOffStats
			elif(att.get_attribute('title') == 'Yellow cards'):
				return yellowStats
			elif(att.get_attribute('title') == 'Second yellow cards'):
				return yellowRedStats
			elif(att.get_attribute('title') == 'Red cards'):
				return redStats
			elif(att.get_attribute('title') == 'Minutes played'):
				return minutesPlayedStats
			elif(att.get_attribute('title') == 'Assists'):
				return assistStats
			elif(att.get_attribute('title') == 'Penalty goals'):
				return penaltyGoalsStats
			elif(att.get_attribute('title') == 'Minutes per goal'):
				return mpgStats

		for attribute in attributes:

			value = GetValueOfAttribute(attribute)
			att = attribute.get_attribute('title')
			for i in range(len(competitions)):
				compToApp = competitions[i].text
				try:
					valToApp = value[i].text
				except TypeError:
					valToApp = '-'

				statsData = statsData.append({'Player_Id': playerId, 'Name': name, 'Position': pos, 'Competition': compToApp, 'Attribute': att, 'Value': valToApp}, ignore_index=True)

		statsData.to_csv('./Scrapped_Data/natstats.csv', mode='a', header=False)
		driver.find_element_by_xpath("//*[(@id = 'profile')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'megamenu', ' ' ))]").click()

		time.sleep(2)

	if(pos == 'Goalkeeper'):
		getGkInternStats(playerId)
	else:
		getInternStats(playerId)

	try:
		driver.find_element_by_xpath("//*[(@id = 'national-team')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'megamenu', ' ' ))]").click()
		driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'box', ' ' )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'kartei-number-2', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'kartei-button-body', ' ' ))]").click()

		time.sleep(2)

		if(pos == 'Goalkeeper'):
			getGkNatStats(playerId)
		else:
			getNatStats(playerId)
	except:
		driver.find_element_by_xpath("//*[(@id = 'profile')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'megamenu', ' ' ))]").click()
	time.sleep(3)
	try:
		instaLink = driver.find_element_by_xpath("//*[@title='Instagram']").get_attribute("href")
		followers = getFollowers(instaLink).text
	except:
		followers = 'no info'

	playersData = playersData.append({'Id': playerId,'Name': name, 'Team': team, 'Nationality': nat, 'Date of Birth': dob, 'Height': hgt, 'Strong Foot': foot, 'Position': pos, 'Joined': joined, 'Contract Expires': until, 'Followers': followers}, ignore_index = True)

	playersData.to_csv('./Scrapped_Data/Players.csv', mode='a', header=False)


	time.sleep(5)

#def TeamPage(link):
	
#	driver.get(link)
	
#	teamPlayers = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'tooltipstered', ' ' ))]")
#	del teamPlayers[::2]
	
#	for player in teamPlayers:
#		playerLinks.append(player.get_attribute("href"))


#for team in allTeams:
#	teamLinks.append(team.get_attribute("href"))

#for teamLink in teamLinks:
#	TeamPage(teamLink)
numStopped = 125


for row in range(numStopped-2, len(playerLinksData['Name'])):
	link = playerLinksData['Player_url'][row]
	PlayerPage(link,row)

driver.quit()
