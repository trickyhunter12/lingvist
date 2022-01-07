import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json



def get_page_info(pageNummber,id):


    client = MongoClient("mongodb+srv://Shevcenko:Gbz3xXwz6mK5OZur@cluster0.appyb.mongodb.net/lingvist?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    database = client["lingvist"]
    collection = database["news"]
    
    url = 'https://riac34.ru/news/' + '?PAGEN_1=' + str(pageNummber)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    page = soup.find('div', class_='inner-new-content')
    news_date = page.find_all('span', class_='date')
    headlines = page.find_all('a', class_='caption')

    counter = 0
    data = []

    for i in range(0, len(headlines)):
        headline = headlines[i].text #1 заголовок
        site = "https://riac34.ru/" + headlines[i].get('href') #2 ссылка
        responseT = requests.get(site)
        soupT = BeautifulSoup(responseT.text, 'lxml')
        biglineT = soupT.find('div', class_='full-text')
        try:
            newsLine = biglineT.text
        except:
            continue
        replace_val=['\n','\t','\r']
        for k in replace_val:
            newsLine = newsLine.replace(k, "") #3 текст новости
        newsTime = news_date[i].text #4   дата
        statistics = soupT.find('div',class_='new-comm-views')
        views = statistics.find('span',class_='views')
        countViews = views.text
        comments = statistics.find('span',class_='comments')
        countComments = comments.text

        json_data = ({
                "headline": headline,
                "url":site,
                "text": newsLine,
                "date": newsTime,
                "views": countViews,
                "comments": countComments,
                "_id": int(id)+counter+13963 
            })
        
        if collection.find_one({'url': url}) is None:
            collection.insert_one(json_data)
        data.append(json_data)
        counter +=1

    return data


def main():
    data = []
    for i in range (4001,5000):
        id = len(data)
        data += get_page_info(i,id)
        with open("test2.json","w",encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=5)
            f.close()

if __name__ == "__main__":
    main()
