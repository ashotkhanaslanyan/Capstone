from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options= opts)

MVCsvHead = pd.DataFrame(columns = ['Name', 'Club', 'League', 'Season', 'Market Value'])
MVCsvHead.to_csv('./Scrapped_Data/markval.csv', mode='a')

#driver.get("https://www.transfermarkt.com/1-bundesliga/startseite/wettbewerb/L1")

#allTeams = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hide-for-pad', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'tooltipstered', ' ' ))]")

teamLinksData = pd.read_csv('Prerequisit Data/teamlinks.csv')

def TeamPage(link):
	
	for season in range(2005, 2020):
		
		link = link[:-4] + str(season)
		driver.get(link)
		driver.maximize_window()
		driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'kartei-number-2', ' ' ))]//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'kartei-button-body', ' ' ))]").click()

		markVal = pd.DataFrame(columns=['Name', 'Club', 'League', 'Season', 'Market Value'])

		names = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'spielprofil_tooltip', ' ' ))]")[::2]
		club = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'dataName', ' ' ))]//span").text
		league = driver.find_element_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'hauptpunkt', ' ' ))]//a").text
		scrapSeason = str(season)[-2:] + '/' + str(season + 1)[-2:]
		marketValue = driver.find_elements_by_xpath("//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'rechts', ' ' )) and contains(concat( ' ', @class, ' ' ), concat( ' ', 'hauptlink', ' ' ))]")

		for ind in range(len(names)):
			name = names[ind].text
			try:
				mv = marketValue[ind].text
			except TypeError:
				mv = '-'
			markVal = markVal.append({'Name': name, 'Club': club, 'League': league, 'Season': scrapSeason, "Market Value": mv}, ignore_index=True)

		markVal.to_csv('./Scrapped_Data/markval.csv', mode='a', header=False)	

#for team in allTeams:
#	teamLinks.append(team.get_attribute("href"))

for row in range(0, len(teamLinksData['Team_name'])):
	link = teamLinksData['Team_url'][row]
	TeamPage(link)
