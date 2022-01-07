from flask import Flask, render_template, request, jsonify, make_response
import random
import time
import pymongo
import datetime


app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://Shevcenko:Gbz3xXwz6mK5OZur@cluster0.appyb.mongodb.net/lingvist?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
database = client["lingvist"]
collection = database["news"]

res = collection.find()

app.config['JSON_AS_ASCII'] = False

all_items = collection.find()
all_items2 = collection.find()

db = [] 
db2 = [] 

posts = res  

quantity = 10  

for x in all_items:

    news_title = x['headline']
    news_text = x['text']
    news_link = x['url']
    news_date = x['date']

    db.append(["".join(news_title), "".join(news_text), "".join(news_link), "".join(news_date)])

for y in all_items2:
    try:
        news_text = y['text']
        try:
            person = y['Person']
        except:
            person = "не найдено"
        try:
            object = y['Object']
        except:
            object = "не найдено"
            
        sentiment = y['sentiment']
        
        db2.append(["".join(news_text), "".join(person), "".join(object), "".join(sentiment)])
    except:
        continue

@app.route("/")
def index():
    """ Route to render the HTML """
    return render_template("index.html")

@app.route("/tonality", methods=['GET', 'POST'])
def tomita():
    return render_template("tonality.html")

# @app.route("/sinonim", methods=['GET', 'POST'])
# def sinonim():
#     return render_template("sinonim.html")

@app.route("/load")
def load():
    """ Route to return the posts """

    time.sleep(0.2) 

    if request.args:
        counter = int(request.args.get("c"))  

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
           
            res = make_response(jsonify(db[0: quantity]), 200)

        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print(f"Returning posts {counter} to {counter + quantity}")
           
            res = make_response(jsonify(db[counter: counter + quantity]), 200)

    return res

@app.route("/load1")
def load1():
    """ Route to return the posts """

    time.sleep(0.2)  

    if request.args:
        counter = int(request.args.get("c"))  

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            
            res = make_response(jsonify(db2[0: quantity]), 200)

        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print(f"Returning posts {counter} to {counter + quantity}")
            
            res = make_response(jsonify(db2[counter: counter + quantity]), 200)
    return res

# @app.route("/load2")
# def load2():
#     """ Route to return the posts """

#     time.sleep(0.2)  

#     if request.args:
#         counter = int(request.args.get("c"))  

#         if counter == 0:
#             print(f"Returning posts 0 to {quantity}")
            
#             res = make_response(jsonify(db3[0: quantity]), 200)

#         elif counter == posts:
#             print("No more posts")
#             res = make_response(jsonify({}), 200)

#         else:
#             print(f"Returning posts {counter} to {counter + quantity}")
            
#             res = make_response(jsonify(db3[counter: counter + quantity]), 200)
#     return res
if __name__ == '__main__':
    app.run(debug=True)