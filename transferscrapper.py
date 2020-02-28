from selenium import webdriver
import pandas as pd
import time

csvHead = pd.DataFrame(columns=['Name', 'From', 'To', 'Fee', 'Market Value', 'Season', 'Date'])
csvHead.to_csv('Transfers.csv', mode='a')

driver = webdriver.Firefox()
driver.get("https://www.transfermarkt.com/1-bundesliga/startseite/wettbewerb/L1")

allTeams = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hide-for-pad', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'tooltipstered', ' ' ))]")

teamLinks = []

def PlayerPage(link):
	
	transfersData = pd.DataFrame(columns=['Name', 'From', 'To', 'Fee', 'Market Value', 'Season', 'Date'])

	driver.get(link)

	time.sleep(10)

	name = driver.find_element_by_xpath("//h1").text

	driver.find_element_by_xpath("//*[@id = 'transfers']").click()

	numOfTransfers = len(driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zeile-transfer', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hide-for-small', ' ' )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]"))

	transferSeasons = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zeile-transfer', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hide-for-small', ' ' )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]")
	transferDates = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zeile-transfer', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zentriert', ' ' ))]")
	del transferDates[::3]
	del transferDates[1::2]
	teamLeft = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'vereinsname', ' ' )) and (((count(preceding-sibling::*) + 1) = 6) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'tooltipstered', ' ' ))]")
	teamJoined = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'vereinsname', ' ' )) and (((count(preceding-sibling::*) + 1) = 10) and parent::*)]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'tooltipstered', ' ' ))]")
	markVals = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zeile-transfer', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zelle-mw', ' ' ))]")
	fees = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zeile-transfer', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'zelle-abloese', ' ' ))]")

	for i in range(numOfTransfers):

		transfersData = transfersData.append({'Name': name, 'From': teamLeft[i].text, 'To': teamJoined[i].text, 'Fee': fees[i].text, 'Market Value': markVals[i].text, 'Season': transferSeasons[i].text, 'Date': transferDates[i].text}, ignore_index=True)
	
	transfersData.to_csv('Transfers.csv', mode='a', header=False)

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