import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import numpy as np

#Defining Location
os.chdir('C:\\Users\\Rohan\\Desktop\\BANDS\\spring20\\R and python\\r and python project\\data')

#Loading the Chrome browser for web scraping 
driver = webdriver.Chrome(executable_path=r'C:\Users\Rohan\Downloads\chromedriver_win32\chromedriver.exe')

#Giving imdb list as an input
##2016## 
url = "https://www.imdb.com/search/title/?title_type=feature&year=2016-01-01,2016-12-31&sort=boxoffice_gross_us,desc&ref_=adv_prv"
##2016_2## url = "https://www.imdb.com/search/title/?title_type=feature&year=2016-01-01,2016-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt"
##2017## url="https://www.imdb.com/search/title/?title_type=feature&year=2017-01-01,2017-12-31&sort=boxoffice_gross_us,desc"
##2017_2## url="https://www.imdb.com/search/title/?title_type=feature&year=2017-01-01,2017-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt"
##2018## url="https://www.imdb.com/search/title/?title_type=feature&year=2018-01-01,2018-12-31&sort=boxoffice_gross_us,desc"
##20118_2## url="https://www.imdb.com/search/title/?title_type=feature&year=2018-01-01,2018-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt"

# Defining length
l=50

# Opeining up the list of movie url
driver.get(url)

# Extracting link of movies from the above url  
arr=np.empty((0))
for j in range(0,l):
    collect_xcode='//*[@id="main"]/div/div[3]/div/div['+ str(j+1) +']/div[3]/h3/a'
    url_movie=driver.find_elements_by_xpath(collect_xcode)[0].get_attribute('href')
    arr=np.append(arr,url_movie)
    
# Scraping IMDB information into dataframe
d1=pd.DataFrame()
for i in range(34,l):
    driver.get(arr[i])
    #driver.find_elements_by_xpath(collect_xcode)[0].click()
    driver.refresh()
    time.sleep(3)
    
    
    # Extracting profile link of Director, writer and actor from IMDB movie page
    director_xcode='//div[@class="plot_summary "]/div[2]/a'
    dir_url=driver.find_elements_by_xpath(director_xcode)[0].get_attribute('href')
    Writer_xcode='//div[@class="plot_summary "]/div[3]/a'
    wri_url=driver.find_elements_by_xpath(Writer_xcode)[0].get_attribute('href')
    Actor_xcode='//div[@class="plot_summary "]/div[4]/a'
    act_url=driver.find_elements_by_xpath(Actor_xcode)[0].get_attribute('href')
        
    
    ### Extracting Rating
    rating_xcode='//span[@itemprop="ratingValue"]'
    rating=driver.find_elements_by_xpath(rating_xcode)[0].text
    d1.loc[i,'Rating']=rating
    
    
    ### Checking mentioning of Official Sites for error calculation
    error_xcode='//div[@id="titleDetails"]/div[1]'
    error_elem=driver.find_elements_by_xpath(error_xcode)[0].text
    if(re.search('(Official Sites)|(Official Site)',error_elem)):
        error=0
    else:
        error=1
        
    ### Extracting Release_Date
    Release_Date_xcode='//div[@id="titleDetails"]/div['+str(4-error)+']'
    Release_Date_elem=driver.find_elements_by_xpath(Release_Date_xcode)[0].text
    if(re.search('(USA)',Release_Date_elem)):
        Release_Date_split=Release_Date_elem.split(" ")
        Release_Date = Release_Date_split[2]+" " +Release_Date_split[3]+" "+Release_Date_split[4]
    else:
        Release_Date=""
    d1.loc[i,'Release_Date']=Release_Date   
        
    ### Checking mentioning of Budget for error calculation
    error_xcode='//div[@id="titleDetails"]/div['+str(7)+']'
    error_elem=driver.find_elements_by_xpath(error_xcode)[0].text
    if(re.search('((Budget))',error_elem)):
        error=0
    else:
        error=1
        
    ### Extracting Budget
    Budget_xcode='//div[@id="titleDetails"]/div['+str(7-error)+']'
    Budget_elem=driver.find_elements_by_xpath(Budget_xcode)[0].text
    if(re.search('(Budget)',Budget_elem)):
        Budget = re.search('\$[^ ]*',Budget_elem).group(0)
        Budget=Budget
    else:
        Budget=""
    d1.loc[i, "Budget"]=Budget

        ## Extracting Opening_Week_Collection
    collect_xcode='//div[@id="titleDetails"]/div['+str(8-error)+']'
    collect_elem=driver.find_elements_by_xpath(collect_xcode)[0].text
    if(re.search('(USA)',collect_elem)):
        collect = re.search('\$[^ ]*',collect_elem).group(0)
        collect=collect[0:-1]
    else:
        collect=""
    d1.loc[i,'Opening_Week_Collection']=collect
    
    ### Extracting Country
    Country_xcode='//div[@id="titleDetails"]/div['+str(2-error)+']'
    Country_elem=driver.find_elements_by_xpath(Country_xcode)[0].text
    if(re.search('(Country)',Country_elem)):
        Country_split_1=Country_elem.split(":")
        Country_split_2=Country_split_1[1].split("|")
        Country=Country_split_2[0]
    else:
        Country=""
    d1.loc[i, "Country"]=Country


    ### Extracting Language
    Language_xcode='//div[@id="titleDetails"]/div['+str(3-error)+']'
    Language_elem=driver.find_elements_by_xpath(Language_xcode)[0].text
    if(re.search('(Language)',Language_elem)):
        Language_split_1=Language_elem.split(":")
        Language_split_2=Language_split_1[1].split("|")
        Language=Language_split_2[0]
    else:
        Language=""
    d1.loc[i, "Language"]=Language
    
    
    
    ### Extracting Genre
    Genre_xcode='//div[@id="titleStoryLine"]/div[4]'
    Genre_elem=driver.find_elements_by_xpath(Genre_xcode)[0].text
    if(re.search('(Genres)|(Genre)',Genre_elem)):
        Genre_split_1=Genre_elem.split(":")
        Genre_no=Genre_split_1[1].count("|")+1
        Genre = Genre_split_1[1]
        d1.loc[i,'Genre']=Genre
    else:
        Genre=""
    d1.loc[i,'Genre_no']=Genre_no
    
    ### Extracting Runtime
    Runtime_xcode='//div[@class="subtext"]/time'
    Runtime_elem=driver.find_elements_by_xpath(Runtime_xcode)[0].text
    if(re.search('(min)',Runtime_elem)):
        Runtime_reg = re.findall('[0-9]{1,3}',Runtime_elem)
        Runtime=int(Runtime_reg[0])*60+int(Runtime_reg[1])
    else:
        Runtime=0
    d1.loc[i,'Runtime']=Runtime
    

    
    ### Extracting Title
    Title_xcode='//div[@class="title_wrapper"]/h1'
    Title=driver.find_elements_by_xpath(Title_xcode)[0].text
    d1.loc[i,'Title']=Title
    
    ### Extracting movie link
    d1.loc[i,'Link']=arr[i]

    ### Extracting Director Wins
    driver.get(dir_url)
    time.sleep(1.5)
    #driver.find_elements_by_xpath(director_xcode)[0].click()
    director_award_xcode='//span[@class="awards-blurb"]'
    
    try:
        try:
            director_oscar_elm=driver.find_elements_by_xpath(director_award_xcode)[0].text
            director_oscar = re.search('[0-9]{1,3}',director_oscar_elm).group(0)
            director_win_elm=driver.find_elements_by_xpath(director_award_xcode)[1].text
            director_win = re.search('[0-9]{1,4}',director_win_elm).group(0)
            if(not(re.search('(wins)|(win)',director_win_elm))):
                director_win=0
        except IndexError:
            director_oscar=0
            director_win_elm=driver.find_elements_by_xpath(director_award_xcode)[0].text
            director_win = re.search('[0-9]{1,4}',director_win_elm).group(0)
            if(not(re.search('(wins)|(win)',director_win_elm))):
                director_win=0
    except IndexError:
        director_oscar=0
        director_win=0
    
    d1.loc[i,'Director_Oscar']=director_oscar
    d1.loc[i,'Director_Wins']=director_win

    
    
    ### Extracting Writer Wins
    driver.get(wri_url)
    time.sleep(1.5)
    #driver.find_elements_by_xpath(Writer_xcode)[0].click()
    Writer_award_xcode='//span[@class="awards-blurb"]'
    
    try:
        try:
            Writer_oscar_elm=driver.find_elements_by_xpath(Writer_award_xcode)[0].text
            Writer_oscar = re.search('[0-9]{1,3}',Writer_oscar_elm).group(0)
            Writer_win_elm=driver.find_elements_by_xpath(Writer_award_xcode)[1].text
            Writer_win = re.search('[0-9]{1,4}',Writer_win_elm).group(0)
            if(not(re.search('(wins)|(win)',Writer_win_elm))):
                Writer_win=0
        except IndexError:
            Writer_oscar=0
            Writer_win_elm=driver.find_elements_by_xpath(Writer_award_xcode)[0].text
            Writer_win = re.search('[0-9]{1,4}',Writer_win_elm).group(0)
            if(not(re.search('(wins)|(win)',Writer_win_elm))):
                Writer_win=0
    except IndexError:
        Writer_oscar=0
        Writer_win=0
    
    d1.loc[i,'Writer_Oscar']=Writer_oscar
    d1.loc[i,'Writer_Wins']=Writer_win

    
    
    ### Extracting Actor Wins
    driver.get(act_url)
    time.sleep(1.5)
    #driver.find_elements_by_xpath(Actor_xcode)[0].click()
    Actor_award_xcode='//span[@class="awards-blurb"]'
    
    try:
        try:
            Actor_oscar_elm=driver.find_elements_by_xpath(Actor_award_xcode)[0].text
            Actor_oscar = re.search('[0-9]{1,3}',Actor_oscar_elm).group(0)
            Actor_win_elm=driver.find_elements_by_xpath(Actor_award_xcode)[1].text
            Actor_win = re.search('[0-9]{1,4}',Actor_win_elm).group(0)
            if(not(re.search('(wins)|(win)',Actor_win_elm))):
                Actor_win=0
        except IndexError:
            Actor_oscar=0
            Actor_win_elm=driver.find_elements_by_xpath(Actor_award_xcode)[0].text
            Actor_win = re.search('[0-9]{1,4}',Actor_win_elm).group(0)
            if(not(re.search('(wins)|(win)',Actor_win_elm))):
                Actor_win=0
    except IndexError:
        Actor_oscar=0
        Actor_win=0
    
    d1.loc[i,'Actor_Oscar']=Actor_oscar
    d1.loc[i,'Actor_Wins']=Actor_win


###Saving to excel file
d1.to_excel("final2018.xlsx")
    
