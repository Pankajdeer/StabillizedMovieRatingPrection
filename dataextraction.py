import pandas as pd
import re

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
d1=pd.DataFrame()

//*[@id="main"]/div/div[3]/div[3]/div[1]/div[2]/h3/a


url = "https://www.imdb.com/title/tt1712261/?ref_=ttls_li_tt"
driver = webdriver.Firefox(executable_path=r'C:\Users\Rohan\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe')
driver.get(url)



## Opening_Week_Collection
collect_xcode='//div[@id="titleDetails"]/div[8]'
collect_elem=driver.find_elements_by_xpath(collect_xcode)[0].text
if(re.search('(USA)',collect_elem).group(0)):
    collect = re.search('\$[^ ]*',collect_elem).group(0)
    collect=collect[0:-1]
else:
    collect=""
d1.loc[0,'Opening_Week_Collection']=collect

### Director_no_of_awards
director_xcode='//div[@class="plot_summary "]/div[2]/a'
driver.find_elements_by_xpath(director_xcode)[0].click()
director_award_xcode='//span[@class="awards-blurb"]'

try:
    try:
        director_oscar_elm=driver.find_elements_by_xpath(director_award_xcode)[0].text
        director_oscar = re.search('[0-9]{1,3}',director_oscar_elm).group(0)
        director_win_elm=driver.find_elements_by_xpath(director_award_xcode)[1].text
        director_win = re.search('[0-9]{1,4}',director_win_elm).group(0)
        if(not(re.search('(wins)|(win)',director_win_elm).group(0))):
            director_win=0
    except IndexError:
        director_oscar=0
        director_win_elm=driver.find_elements_by_xpath(director_award_xcode)[0].text
        director_win = re.search('[0-9]{1,4}',director_win_elm).group(0)
        if(not(re.search('(wins)|(win)',director_win_elm).group(0))):
            director_win=0
except IndexError:
    director_oscar=0
    director_win=0

d1.loc[0,'Director_Oscar']=director_oscar
d1.loc[0,'Director_Wins']=director_win
driver.get(url)


### Writer_no_of_awards
Writer_xcode='//div[@class="plot_summary "]/div[3]/a'
driver.find_elements_by_xpath(Writer_xcode)[0].click()
Writer_award_xcode='//span[@class="awards-blurb"]'

try:
    try:
        Writer_oscar_elm=driver.find_elements_by_xpath(Writer_award_xcode)[0].text
        Writer_oscar = re.search('[0-9]{1,3}',Writer_oscar_elm).group(0)
        Writer_win_elm=driver.find_elements_by_xpath(Writer_award_xcode)[1].text
        Writer_win = re.search('[0-9]{1,4}',Writer_win_elm).group(0)
        if(not(re.search('(wins)|(win)',Writer_win_elm).group(0))):
            Writer_win=0
    except IndexError:
        Writer_oscar=0
        Writer_win_elm=driver.find_elements_by_xpath(Writer_award_xcode)[0].text
        Writer_win = re.search('[0-9]{1,4}',Writer_win_elm).group(0)
        if(not(re.search('(wins)|(win)',Writer_win_elm).group(0))):
            Writer_win=0
except IndexError:
    Writer_oscar=0
    Writer_win=0

d1.loc[0,'Writer_Oscar']=Writer_oscar
d1.loc[0,'Writer_Wins']=Writer_win
driver.get(url)



### Actor_no_of_awards
Actor_xcode='//div[@class="plot_summary "]/div[4]/a'
driver.find_elements_by_xpath(Actor_xcode)[0].click()
Actor_award_xcode='//span[@class="awards-blurb"]'

try:
    try:
        Actor_oscar_elm=driver.find_elements_by_xpath(Actor_award_xcode)[0].text
        Actor_oscar = re.search('[0-9]{1,3}',Actor_oscar_elm).group(0)
        Actor_win_elm=driver.find_elements_by_xpath(Actor_award_xcode)[1].text
        Actor_win = re.search('[0-9]{1,4}',Actor_win_elm).group(0)
        if(not(re.search('(wins)|(win)',Actor_win_elm).group(0))):
            Actor_win=0
    except IndexError:
        Actor_oscar=0
        Actor_win_elm=driver.find_elements_by_xpath(Actor_award_xcode)[0].text
        Actor_win = re.search('[0-9]{1,4}',Actor_win_elm).group(0)
        if(not(re.search('(wins)|(win)',Actor_win_elm).group(0))):
            Actor_win=0
except IndexError:
    Actor_oscar=0
    Actor_win=0

d1.loc[0,'Actor_Oscar']=Actor_oscar
d1.loc[0,'Actor_Wins']=Actor_win
driver.get(url)



### Rating
rating_xcode='//span[@itemprop="ratingValue"]'
rating=driver.find_elements_by_xpath(rating_xcode)[0].text
d1.loc[0,'Rating']=rating


### Release_Date
Release_Date_xcode='//div[@id="titleDetails"]/div[4]'
Release_Date_elem=driver.find_elements_by_xpath(Release_Date_xcode)[0].text
if(re.search('(USA)',Release_Date_elem).group(0)):
    Release_Date_split=Release_Date_elem.split(" ")
    Release_Date = Release_Date_split[2]+" " +Release_Date_split[3]+" "+Release_Date_split[4]
else:
    Release_Date=""
d1.loc[0,'Release_Date']=Release_Date
    
    

### Budget
Budget_xcode='//div[@id="titleDetails"]/div[7]'
Budget_elem=driver.find_elements_by_xpath(Budget_xcode)[0].text
if(re.search('(Budget)',Budget_elem).group(0)):
    Budget = re.search('\$[^ ]*',Budget_elem).group(0)
    Budget=Budget[0:-1]
else:
    Budget=""
d1.loc[0, "Budget"]=Budget


### Genre
Genre_xcode='//div[@id="titleStoryLine"]/div[4]'
Genre_elem=driver.find_elements_by_xpath(Genre_xcode)[0].text
if(re.search('(Genres)|(Genre)',Genre_elem).group(0)):
    Genre_split_1=Genre_elem.split(":")
    Genre_no=Genre_split_1[1].count("|")+1
    Genre = Genre_split_1[1]
    d1.loc[0,'Genre']=Genre
else:
    Genre=""
d1.loc[0,'Genre_no']=Genre_no

### Runtime
Runtime_xcode='//div[@class="subtext"]/time'
Runtime_elem=driver.find_elements_by_xpath(Runtime_xcode)[0].text
if(re.search('(min)',Runtime_elem).group(0)):
    Runtime_reg = re.findall('[0-9]{1,3}',Runtime_elem)
    Runtime=int(a[0])*60+int(a[1])
else:
    Runtime=0
d1.loc[0,'Runtime']=Runtime

### Country
Country_xcode='//div[@id="titleDetails"]/div[2]'
Country_elem=driver.find_elements_by_xpath(Country_xcode)[0].text
if(re.search('(Country)',Country_elem).group(0)):
    Country_split_1=Country_elem.split(":")
    Country_split_2=Country_split_1[1].split("|")
    Country=Country_split_2[0]
else:
    Country=""
d1.loc[0, Country]=Country

### Language
Language_xcode='//div[@id="titleDetails"]/div[3]'
Language_elem=driver.find_elements_by_xpath(Language_xcode)[0].text
if(re.search('(Language)',Language_elem).group(0)):
    Language_split_1=Language_elem.split(":")
    Language_split_2=Language_split_1[1].split("|")
    Language=Language_split_2[0]
else:
    Language=""
d1.loc[0, Language]=Language


### Title
Title_xcode='//div[@class="title_wrapper"]/h1'
Title=driver.find_elements_by_xpath(Title_xcode)[0].text
d1.loc[0,'Title']=Title

###link
d1.loc[0,'Link']=url


###Saving to excel file
d1.to_excel("d1.xlsx")

