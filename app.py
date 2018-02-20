from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.missiontomars_db
collection = db.missiontomars

@app.route("/")

def index():
	data = mongo.db.missiontomars.find_one()
	return render_template('index.html', listings=data)

@app.route("/scrape")
def scrape():
	missiontomars = mongo.db.missiontomars
	missiontomars_data = scrape_mars.scrape()
	missiontomars.update(
        {},
        missiontomars_data,
        upsert=True
        )
	return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)