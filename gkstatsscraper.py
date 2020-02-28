from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

StatsCsvHead = pd.DataFrame(columns=['Name', 'Position', 'Team', 'Season', 'Competition', 'Attribute', 'Value'])
StatsCsvHead.to_csv('stats.csv', mode='a')

NatCsvHead = pd.DataFrame(columns = ['Name', 'Position', 'Competition', 'Attribute', 'Value'])
NatCsvHead.to_csv('natstats.csv', mode='a')

driver = webdriver.Firefox()
driver.get("https://www.transfermarkt.com/florian-grillitsch/profil/spieler/195736")

time.sleep(10)

name = driver.find_element_by_xpath("//h1").text
pos = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataDaten', ' ' )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//p[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataValue', ' ' ))]").text

driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'leistungsdatenContent', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'swiper-slide-active', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'button', ' ' ))]").click()

filtersDiv = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'large-8', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'content', ' ' ))]")
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

def getGkInternStats():

	global name
	global pos
	
	statsData = pd.DataFrame(columns=['Name', 'Position', 'Team', 'Season', 'Competition', 'Attribute', 'Value'])

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
			print(teamToApp, seasonToApp, compToApp, att, valToApp)
			statsData = statsData.append({'Name': name, 'Position': pos, 'Team': teamToApp, 'Season': seasonToApp, 'Competition': compToApp, 'Attribute': att, 'Value': valToApp}, ignore_index=True)

	statsData.to_csv('stats.csv',mode='a', header = False)

def getGkNatStats():

	global name
	global pos

	statsData = pd.DataFrame(columns=['Name', 'Position', 'Competition', 'Attribute', 'Value'])

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
			print(compToApp, att, valToApp)
			statsData = statsData.append({'Name': name, 'Position': pos, 'Competition': compToApp, 'Attribute': att, 'Value': valToApp}, ignore_index=True)

	statsData.to_csv('natstats.csv', mode='a', header=False)

def getInternStats():

	global name
	global pos

	statsData = pd.DataFrame(columns=['Name', 'Position', 'Team', 'Season', 'Competition', 'Attribute', 'Value'])

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
				velToApp = '-'
			statsData = statsData.append({'Name': name, 'Position': pos, 'Team': teamToApp, 'Season': seasonToApp, 'Competition': compToApp, 'Attribute': att, 'Value': valToApp}, ignore_index=True)

	statsData.to_csv('stats.csv', mode='a', header=False)

def getNatStats():

	global name
	global pos

	statsData = pd.DataFrame(columns=['Name', 'Position', 'Competition', 'Attribute', 'Value'])

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

			statsData = statsData.append({'Name': name, 'Position': pos, 'Competition': compToApp, 'Attribute': att, 'Value': valToApp}, ignore_index=True)

	statsData.to_csv('natstats.csv', mode='a', header=False)

if(pos == 'Goalkeeper'):
	getGkInternStats()
else:
	getInternStats()

try:
	driver.find_element_by_xpath("//*[(@id = 'national-team')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'megamenu', ' ' ))]").click()
	driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'box', ' ' )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'kartei-number-2', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'kartei-button-body', ' ' ))]").click()

	if(pos == 'Goalkeeper'):
		getGkNatStats()
	else:
		getNatStats()

except NoSuchElementException as exception:
	driver.find_element_by_xpath("//*[(@id = 'profile')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'megamenu', ' ' ))]")

driver.quit()