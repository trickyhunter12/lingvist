from pymongo import MongoClient
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

import re, string, random

if __name__ == "__main__":

    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)

    # РћС†РµРЅРєР° РїСЂРµРґР»РѕР¶РµРЅРёР№ РёР· Р‘Р”
    client = MongoClient("mongodb+srv://Shevcenko:Gbz3xXwz6mK5OZur@cluster0.appyb.mongodb.net/lingvist?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    database = client["lingvist"]
    collection = database["news"]
    for news in collection.find( {} ): 
        text = [str(news['text'])]
        result = model.predict(text, k=2)
        try:
            person = news["Person"]
        except:
            person = ""
        try:
            attraction = news["Object"]
        except:
            attraction = ""
        if person != "" or attraction != "":       # РµСЃС‚СЊ Рё РїРµСЂСЃРѕРЅР°, Рё РґРѕСЃС‚РѕРїСЂРёРјРµС‡Р°С‚РµР»СЊРЅРѕСЃС‚СЊ
            collection.update({
            "_id": news["_id"]
            }, {
            "$push":{
            "sentiment": result[0]
                    }
            })