# coding=utf-8


# usage : python3 clean_twetts_csv > output.txt
# Mohamed BEN ALI -- Data Scientist - Data Engineer 


# import lib - pandas - nltk  - string

import re
import pandas as pd 
import numpy as np 
import string
import nltk
from nltk.stem.porter import *
import warnings 
from datetime import datetime as dt

warnings.filterwarnings("ignore", category=DeprecationWarning)

tweets = pd.read_csv(r'data.csv')
df = pd.DataFrame(tweets, columns = ['date','text'])

df['date'] = pd.to_datetime(df['date']).dt.date #changing date to datetime format from time-series

#removing pattern from tweets

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt   

# remove twitter handles (@user)
tweets['clean_tweet'] = np.vectorize(remove_pattern)(tweets['text'], "@[\w]*")
#remove urls    
tweets['clean_tweet'] = np.vectorize(remove_pattern)(tweets['text'], "https?://[A-Za-z./]*")

## remove special characters, numbers, punctuations
tweets['clean_tweet'] = tweets['clean_tweet'].str.replace("[^a-zA-Z#]", " ")
tweets['clean_tweet'] = tweets['clean_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>2]))  



print(tweets)
