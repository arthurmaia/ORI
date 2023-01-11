import unidecode
import pandas as pd
from textblob import TextBlob
import demoji
import re
from translate import Translator


def returnBoWFromFilePathWithoutStopWordsWithStemming(phrase):

    phrase = re.sub(
        '((https|http|ftp|www|www1)?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*',
        '', phrase)
    phrase = phrase.lower().replace(',', ' ').replace('.', ' ').replace(
        '"',
        ' ').replace('!', ' ').replace('?', ' ').replace('(', ' ').replace(
            ')',
            ' ').replace('/', ' ').replace('#', ' ').replace('@', ' ').replace(
                '-', ' ').replace(';', ' ').replace("'", ' ').replace(
                    ':', ' ').replace('$', ' ').replace('%', ' ').replace(
                        '&', ' ').replace('*', ' ').replace('_', ' ').replace(
                            '=', ' ').replace('+', ' ').replace(
                                '[', ' ').replace(']', ' ').replace(
                                    '{', ' ').replace('}', ' ').replace(
                                        '<', ' ').replace('>', ' ')

    demoji.findall(phrase)
    demoji.replace(phrase, ' ')
    phrase = unidecode.unidecode(phrase)

    return phrase


df = pd.read_csv('reforma_previdencia_rotulado.csv',
                 sep=';',
                 usecols=['Tweet', 'Classificação'])


class ResponseCSV:
    Tweet = []
    FellingValue = []


response = ResponseCSV()
translator = Translator(from_lang='pt', to_lang='en')

for index, row in df.iterrows():
    phraseOrigins = df.iloc[index]['Tweet']

    phraseCleared = returnBoWFromFilePathWithoutStopWordsWithStemming(
        phraseOrigins)

    phraseEn = translator.translate(phraseCleared)
    print(phraseEn)
    fellingValue = TextBlob(phraseEn)

    response.Tweet.append(phraseCleared)

    response.FellingValue.append(fellingValue.sentiment.polarity)

responses = {'Tweet': response.Tweet, 'FeelingValue': response.FellingValue}

newDf = pd.DataFrame(responses)
newDf.to_csv("response.csv", sep='|')
print(newDf)
