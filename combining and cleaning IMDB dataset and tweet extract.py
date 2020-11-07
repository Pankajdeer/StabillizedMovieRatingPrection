import pandas as pd
import numpy as np
import os
import datetime
import twint
import nest_asyncio
nest_asyncio.apply()
import time
import glob

#Defining Location
os.chdir('C:\\Users\\Rohan\\Desktop\\BANDS\\spring20\\R and python\\r and python project\\data')


#Loading all IMDB dataset into dataframe
d1=pd.read_excel("final2016_1.xlsx",index_col=0)
d2=pd.read_excel("final2016_2.xlsx",index_col=0)
d3=pd.read_excel("final2017_1.xlsx",index_col=0)
d4=pd.read_excel("final2017_2.xlsx",index_col=0)
d6=pd.read_excel("final2018.xlsx",index_col=0)
d7=pd.read_excel("final2018_2.xlsx",index_col=0)

#Combining all the above dataset into one
d5=pd.concat([d1,d2,d3,d4,d6,d7])

#Converting Released date into datetime format for further processing
d5.Release_Date=pd.to_datetime(d5.Release_Date)

#Reseting the index
d5=d5.reset_index()

#Cleaning Budget column so that it can be used as numerical type
d5.Budget=d5.Budget.str.replace('$','')
d5.Budget=d5.Budget.str.replace(',','').astype(int)

#Cleaning Opening weekend collection column so that it can be used as numerical type
d5.Opening_Week_Collection=d5.Opening_Week_Collection.str.replace('$','')
d5.Opening_Week_Collection=d5.Opening_Week_Collection.str.replace(',','').astype(int)

# Cleaning country column
d5.Country=d5.Country.str.replace(' ','')

# Subsetting the data to only US
d5=d5.loc[d5.Country=='USA',:]

# Extracting the first genre
d5['First_Genre']=d5.Genre.str.extract("([A-z]+)")

#Drop any missing value records
d5=d5.dropna()
d5=d5.reset_index()
d5=d5.drop(d5.columns[0],axis=1)
d5=d5.drop('index',axis=1)


#Cleaning language column
d5.Language=d5.Language.str.replace(' ','')

# Cleaning title columsn
d5.Title=d5.Title.str.replace(r'(\([^\n]+\))','')
d5.Title=d5.Title.str.replace(':','')
d5.Title=d5.Title.str.replace('?','')

#Saving file to excel
d5.to_excel('final_data_side.xlsx')

# reading flie
d5=pd.read_excel('final_data_side.xlsx',index_col=0)



# Extracting tweets
os.chdir('D:\\project')
i=0
p=1
while(i<=len(d5)):
    try:
        print(i)
        c=0
        c = twint.Config()
        c.Search = d5.Title[i]
        c.Lang="en"
        c.Limit = 5000
        c.Since  = d5.Release_Date[i].strftime("%Y-%m-%d")
        c.Until  = (d5.Release_Date[i] + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        c.Store_csv=True
        c.Output = d5.Title[i][0:-1] +'.csv'
        twint.run.Search(c)
        time.sleep(300)
    except KeyError:
        print("error",i)
        #time.sleep(300)
    else:
        #time.sleep(300)
        print("else",i)
   
        
    # Flag to check if file was created
    if glob.glob(d5.Title[i][0:-1] +'.csv'):
        p=0
        i=i+1
    elif (not glob.glob(d5.Title[i][0:-1] +'.csv')) and p==0:
        p=1
        i=i-1
        os.remove(d5.Title[i][0:-1] +'.csv')
        time.sleep(600)
    else:
        time.sleep(600)





