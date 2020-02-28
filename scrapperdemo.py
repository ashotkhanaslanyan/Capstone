from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidArgumentException
import pandas as pd

playersData = pd.DataFrame(columns=['Name', 'Team', 'Nationality', 'Date of Birth', 'Height', 'Strong Foot', 'Position', 'Joined', 'Contract Expires', 'Followers'])

driver = webdriver.Firefox()
driver.get("https://www.transfermarkt.com/robert-lewandowski/profil/spieler/38253")

infoTags = [driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'auflistung', ' ' ))]//th"), driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'auflistung', ' ' ))]//td")]

def getNat():
	
	global infoTags

	for key in infoTags[0]:
		if(key.text == 'Citizenship:'):
			ind = infoTags[0].index(key)
			return infoTags[1][ind]

def getFoot():

	global infoTags

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
foot = getFoot().text
instaLink = driver.find_element_by_xpath("//*[@title='Instagram']").get_attribute("href")
followers = getFollowers(instaLink).text

playersData = playersData.append({'Name': name, 'Team': team, 'Nationality': nat, 'Date of Birth': dob, 'Height': hgt, 'Strong Foot': foot, 'Position': pos, 'Joined': joined, 'Contract Expires': until, 'Followers': followers}, ignore_index = True)

driver.close()

playersData.to_csv('Players.csv')