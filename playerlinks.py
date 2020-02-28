from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.firefox.options import Options
import time

# teamCount = 18

# while(teamCount > 0):

opts = Options()
opts.headless = True

driver = webdriver.Firefox(options=opts)

leagueLink = "https://www.transfermarkt.com/major-league-soccer/startseite/wettbewerb/MLS1"

driver.get(leagueLink)

allTeams = ["https://www.transfermarkt.com/aek-athen/startseite/verein/2441", "https://www.transfermarkt.com/al-ain-fc/startseite/verein/2150", "https://www.transfermarkt.com/zska-moskau/startseite/verein/2410", "https://www.transfermarkt.com/gnk-dinamo-zagreb/startseite/verein/419", "https://www.transfermarkt.com/dynamo-kiew/startseite/verein/338", "https://www.transfermarkt.com/hjk-helsinki/startseite/verein/1008", "https://www.transfermarkt.com/kaizer-chiefs/startseite/verein/568", "https://www.transfermarkt.com/lokomotiv-moskau/startseite/verein/932", "https://www.transfermarkt.com/olympiakos-piraus/startseite/verein/683", "https://www.transfermarkt.com/orlando-pirates/startseite/verein/2557", "https://www.transfermarkt.com/panathinaikos-athen/startseite/verein/265", "https://www.transfermarkt.com/paok-thessaloniki/startseite/verein/1091", "https://www.transfermarkt.com/shakhtar-donetsk/startseite/verein/660", "https://www.transfermarkt.com/ac-sparta-prag/startseite/verein/197", "https://www.transfermarkt.com/sk-slavia-prag/startseite/verein/62", "https://www.transfermarkt.com/spartak-moskau/startseite/verein/232", "https://www.transfermarkt.com/fc-viktoria-pilsen/startseite/verein/941"]
allTeams[len(allTeams)//2:]

teamLinks = []

def TeamPage(link):

	global playerLinksCsv

	driver.get(link)

	teamPlayers = driver.find_elements_by_xpath("//*[(@id = 'yw1')]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'tooltipstered', ' ' ))]")
	del teamPlayers[1::2]

	for player in teamPlayers:
		
		playerLinksCsv = pd.DataFrame(columns = ['Player Name', 'Player Link'])
		playerLinksCsv = playerLinksCsv.append({'Player Name': player.text, 'Player Link': player.get_attribute("href")}, ignore_index=True)
		playerLinksCsv.to_csv('playerlinks.csv', mode='a', header=False)


for team in allTeams:
	
	teamLinksCsv = pd.DataFrame(columns = ['Team Name', 'Team Link'])
	teamLinks.append(team)
	teamLinksCsv = teamLinksCsv.append({'Team Name': 'Fill in','Team Link': team}, ignore_index=True)
	teamLinksCsv.to_csv('teamlinks.csv', mode='a', header=False)

for teamLink in teamLinks:
	
	TeamPage(teamLink)

driver.quit()

# teamCount -= 1
