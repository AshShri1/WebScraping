import pymongo
from flask import Flask, render_template, redirect

import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.missionmars_db
collection = db.missionmars_db.marscollection


app = Flask(__name__)

@app.route("/")
def home():
    data = list(collection.find({}).sort("date", pymongo.DESCENDING).limit(1))
    latest_data = data[0]
    return render_template('index.html',mars=latest_data)


@app.route("/scrape")
def scrape():
    
    scraped_data = missiontomars.scrape()
    collection.insert_one(scraped_data)
    data = collection.find_one({})
    print(data)
    return render_template('index.html',mars=scraped_data)

if __name__ == "__main__":
    app.run(debug=True)