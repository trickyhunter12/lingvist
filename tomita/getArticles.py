from pymongo import MongoClient
import os

os.chdir('/home/vagrant/tomita-parser/build/bin') 
client = MongoClient("mongodb+srv://Shevcenko:Gbz3xXwz6mK5OZur@cluster0.appyb.mongodb.net/lingvist?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
database = client["lingvist"]
collection = database["news"]
tomita = database["tomita"]

for news in collection.find( {} ): 
    with open("Articles.txt","w") as f:
        #print(news['text'])
        f.write(news['text'])
    
    os.system("./tomita-parser sema.proto") 
    person, object = [],[]
    place = ""
    with open("output.txt","r") as f:
        foutput = f.read()
        words = foutput.split()
        for i in range(len(words)):
            if words[i] == "Person_output":
                if words[i+2] not in person:
                    person.append(words[i+2])
            elif words[i] == "Object_output":
                while words[i+2] != "}":
                    place += words[i+2] + " "
                    i+=1
                place = place[0:-1]
                if place not in object:
                    object.append(place)
               
    for i in range(len(person)):            
        collection.update({
                "_id": news["_id"]
            }, {
                "$pull": {
                "Person": person[i] 
                }
            }) 

    for i in range(len(object)):            
        collection.update({
                "_id": news["_id"]
            }, {
                "$pull": {
                "Object": object[i] 
                }
            }) 

    for i in range(len(person)):
        collection.update({
            "_id": news["_id"]
        }, {
            "$push": {
            "Person": person[i] 
            }
        }) 
    
    for i in range(len(object)):
        collection.update({
            "_id": news["_id"]
        }, {
            "$push": {
            "Object": object[i] 
            }
        }) 

    person.clear()
    object.clear()

