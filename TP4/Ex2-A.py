import unidecode
import pandas as pd
from textblob import TextBlob
import demoji
import re

df = pd.read_csv('response.csv', sep='|', usecols=['Tweet', 'FeelingValue'])


class ResponseCSV:
    Tweet = []
    FellingValue = []


response = ResponseCSV()

for index, row in df.iterrows():
    phrase = df.iloc[index]['Tweet']
    sentiment = float(df.iloc[index]['FeelingValue'])
    sentimentRotuled = ''
    if sentiment >= -1 and sentiment < -0.5:
        sentimentRotuled = "Negativo"
    elif sentiment >= -0.5 and sentiment < 0.5:
        sentimentRotuled = "Neutro"
    elif sentiment >= 0.5 and sentiment <= 1:
        sentimentRotuled = "Positivo"

    response.Tweet.append(phrase)
    response.FellingValue.append(sentimentRotuled)

responses = {'Tweet': response.Tweet, 'Classificação': response.FellingValue}

newDf = pd.DataFrame(responses)
newDf.to_csv("responseClassificado.csv", sep='|')
