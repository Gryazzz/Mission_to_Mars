from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo

mars = Flask(__name__)

mongo = PyMongo(mars)

@mars.route('/')
def home():
    mars_info = mongo.db.collection.find()
    return render_template("index.html", mars_info = mars_info)

@mars.route('/scrape')
def scrape():

    import scrape_mars
    scraped_data = scrape_mars.scrape()

    mongo.db.collection.insert_one(scraped_data)

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    mars.run(debug=True)
