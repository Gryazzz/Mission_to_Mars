from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import flask_pymongo


mars = Flask(__name__)

mongo = PyMongo(mars)

@mars.route('/')
def home():

    mars_info = list(mongo.db.marsdata.find())
    print(mars_info[-1])
    
    return render_template("index.html", mars_info = mars_info[-1])

@mars.route('/scrape')
def scrape():

    import scrape_mars
    scraped_data = scrape_mars.scrape_mars()

    mongo.db.marsdata.insert_one(scraped_data)
    print('data is inserted into mongo')

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    mars.run(debug=True)

