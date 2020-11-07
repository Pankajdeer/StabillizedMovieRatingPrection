from textblob import TextBlob
import pandas as pd
import numpy as np
import os
import math

#Defining Location
os.chdir('D:\\project')

#Reading IMDB dataset into dataframe
d5=pd.read_excel('final_data.xlsx',index_col=0)


#Calculate the % postive,neutral and negative tweets for each movie 
for i in range(0,len(d5)):
    print(i)
    d1=pd.read_csv(d5.Title[i][0:-1] +'.csv')
    
    # Finding out sentiment score for each tweet
    q=d1.tweet.apply(lambda x: math.ceil(TextBlob(x).sentiment.polarity) if TextBlob(x).sentiment.polarity>=0 else -1)
    
    # Aggregating above score on a movie level
    d5.loc[i,"Postive_%"]=q[q==1].count()/q.count()
    d5.loc[i,"Negative_%"]=q[q==-1].count()/q.count()
    d5.loc[i,"Neutral_%"]=q[q==0].count()/q.count()
    
    #Flag to check for error when sum is not equal to 1
    if (q[q==1].count()/q.count() + q[q==-1].count()/q.count() + q[q==0].count()/q.count())==1:
        d5.loc[i,"Flag"]=1
    else:
        d5.loc[i,"Flag"]=0
        
###Saving to CSV file
d5.to_csv("IMDB_side.csv")
