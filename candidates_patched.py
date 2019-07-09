# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 14:54:29 2019
@author: Pipo
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import random

import pause as pos
import pandas as pd

def debug():
    print("debug started")
    
def main():
    
    print("Started" )   
    loginURL = "https://www.linkedin.com/uas/login"
    
    scrapeOC = "https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22pr%3A9349%22%5D&facetIndustry=%5B%2225%22%5D&origin=FACETED_SEARCH"
    
    scrapeUSCA = "https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22us%3A0%22%2C%22ca%3A0%22%5D&facetIndustry=%5B%2225%22%5D&origin=FACETED_SEARCH"
    
    scrapePR = ''
    
    with open('un.txt', 'r') as file:
        user = file.read().replace('\n', '')
    
    with open('passw.txt', 'r') as file:
        passw = file.read().replace('\n', '')
    
    
    driver = webdriver.Firefox()
    
    logIn(driver, loginURL, user, passw)
    
    pos.seconds(3)
    
    #scrape todos los paises excepto canada y US
    scrape(driver, scrapeOC, "_otherCountries.csv")
    
#    pos.seconds(3)
##    
##    #scrape canada y us
#    scrape(driver, scrapeUSCA, "_UsAndCanada.csv")
    
def logIn(driver, loginURL, X,Z):
    
    driver.get(loginURL)
    
    uin = driver.find_element_by_xpath('//*[@id="username"]')
    uin.clear()
    pos.seconds(1)
    uin.send_keys(X)
    
    passkey = driver.find_element_by_xpath('//*[@id="password"]')
    passkey.clear()
    pos.seconds(1)
    passkey.send_keys(Z)
    pos.seconds(1)
    passkey.send_keys(Keys.RETURN)
    
    pos.seconds(3)
        
def scrape(driver, url, country):
     
    #final data to csv
    userNamesFinal = list()
    userJobsFinal = list()
    userLocationsFinal = list()
    pairedUserLinksFinal = list()
    
    #declare temp data
    userNames = list()
    userJobs = list()
    userLocations = list()
    userLinks = list()
    pairedUserLinks = list()
    
    firstElem = 0
    lastElem = 10
    
    PROFILE_DETECT = '/in/'
    
    PROFILE_DETECT2 = 'https://www.linkedin.com/in/'
    
    for page in range(1, 3):
        
        randy = random.uniform(0,2)
        
        driver.get(url)
        
        driver.execute_script('window.scrollTo(0,1500)')
        
        pos.seconds(8 + randy)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        print("Page loaded")
        main_window = soup.find("div", {"class": "search-results ember-view"})
    
        list_window = main_window.find("div", {"class": 
            "blended-srp-results-js pt0 pb4 ph0 container-with-shadow"})
        
        findUsers = list_window.findAll("li", {"class": 
            "search-result search-result__occluded-item ember-view"})
        
        # begin new sector
        
        #restart temp data
        userNames = []
        userJobs = []
        userLocations = []
        userLinks = []
        pairedUserLinks = []
        
        # template starts here
        
        for name in range(firstElem,lastElem):
            try:
                app = findUsers[name].find("h3",{"class" : "actor-name-with-distance search-result__title single-line-truncate ember-view"}).find("span", {"class": "name actor-name"}).text
                userNames.append(str(app))
                try:
                    # remove the mutual connection links
                    soup.find('a', class_="li-i18n-linkto search-result__social-proof-link search-result__social-proof-connection-name search-result__social-proof-connection-name--1 t-bold").decompose()
                    try:
                        soup.find('a', class_="li-i18n-linkto search-result__social-proof-link search-result__social-proof-connection-name search-result__social-proof-connection-name--2 t-bold").decompose()
                    except:
                        print("no BS links")
                except:
                    print("no BS link")
                
            except:
                userNames.append('Linkedin Member')
        
        for location in range(firstElem,lastElem):
            try:
                app = findUsers[location].find("p", {"class": "subline-level-2 t-12 t-black--light t-normal search-result__truncate"}).text
                refinedString = app.replace(app[0], "")
                print(refinedString)
                userLocations.append(refinedString)
            except:
                userLocations.append('N/A')
        
        for job in range(firstElem,lastElem):
            try:
                app = findUsers[job].find("p", {"class": "subline-level-1 t-14 t-black t-normal search-result__truncate"}).text
                refinedString = app.replace(",",";").replace(app[0], "")
                refinedStringnew = str(refinedString)
                userJobs.append(refinedStringnew)
            except:
                userJobs.append('N/A')
        
        
        for link in soup.findAll('a', href=True):
            if (PROFILE_DETECT in link['href']):
                fullLink = 'https://www.linkedin.com' + str(link['href'])
                userLinks.append(fullLink)
                print(fullLink)
            elif (PROFILE_DETECT2 in link['href'] ):
                userLinks.append(str(link['href']))
                print(link['href'])
        
        userLinks = list(dict.fromkeys(userLinks)) # remove duplicates
        
        # if userLinks is empty
        
        if (len(userLinks) == 0):
            for nothing in range(firstElem,lastElem):
                pairedUserLinks.append('N/A')
        else:
            index = 0
            for selected_name in range(firstElem,lastElem):
                
                if (userNames[selected_name] not in 'Linkedin Member'):
                    
                    try:
                        this_user = userLinks[index]
                        pairedUserLinks.append(this_user)
                    except:
                        print("nothing")
                        pairedUserLinks.append("N/A")
                    index += 1
                else:
                    pairedUserLinks.append("N/A")

        # end new sector
            
        nextBTN = driver.find_element_by_xpath('//*[@class="artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view"]')
        nextBTN.click()
        
        #append temp data to array
        
        userNamesFinal.extend(userNames)
        pairedUserLinksFinal.extend(pairedUserLinks)
        
        userLocationsFinal.extend(userLocations) # this line seems defective
        
        userJobsFinal.extend(userJobs)
        
        pos.seconds(1)
        nextURL = driver.current_url
        url = nextURL
        
    f = open("lastPage.txt", "a")
    f.write(url)
    f.close()
    
    final_data = pd.DataFrame({
                'USER':userNamesFinal,
                'JOBP':userJobsFinal,
                'LOCT':userLocationsFinal,
                'LINK':pairedUserLinksFinal}) 
    
    
    final_data.append(final_data, ignore_index = True)
    
    csv_string = 'C:\\Users\\Pipo\\Documents\\Python Scripts\\CANDIDATOS\\scraped_candidates' + country
    
    final_data.to_csv(csv_string)
#    final_data.to_csv(csv_string, mode='a', header=False)
    
    
    
    print(final_data)
        
main()