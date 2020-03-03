from selenium import webdriver
import pandas as pd
import time

csvHead = pd.DataFrame(columns=['Name', 'Team', 'Nationality', 'Date of Birth', 'Height', 'Strong Foot', 'Position', 'Joined', 'Contract Expires', 'Followers'])
csvHead.to_csv('Players.csv', mode='a')

driver = webdriver.Firefox()
driver.get("https://www.transfermarkt.com/1-bundesliga/startseite/wettbewerb/L1")

allTeams = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hide-for-pad', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'tooltipstered', ' ' ))]")

teamLinks = []

def PlayerPage(link):
	
	playersData = pd.DataFrame(columns=['Name', 'Team', 'Nationality', 'Date of Birth', 'Height', 'Strong Foot', 'Position', 'Joined', 'Contract Expires', 'Followers'])

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

	try:
		instaLink = driver.find_element_by_xpath("//*[@title='Instagram']").get_attribute("href")
		followers = getFollowers(instaLink).text
	except:
		followers = 'no info'

	playersData = playersData.append({'Name': name, 'Team': team, 'Nationality': nat, 'Date of Birth': dob, 'Height': hgt, 'Strong Foot': foot, 'Position': pos, 'Joined': joined, 'Contract Expires': until, 'Followers': followers}, ignore_index = True)

	playersData.to_csv('Players.csv', mode='a', header=False)

	time.sleep(5)

def TeamPage(link):
	
	driver.get(link)
	
	playerLinks = []
	teamPlayers = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'tooltipstered', ' ' ))]")
	del teamPlayers[::2]
	
	for player in teamPlayers:
		playerLinks.append(player.get_attribute("href"))
	
	for playerLink in playerLinks:
		PlayerPage(playerLink)

for team in allTeams:
	teamLinks.append(team.get_attribute("href"))

for teamLink in teamLinks:
	TeamPage(teamLink)

driver.quit()