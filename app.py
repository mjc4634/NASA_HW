from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo 
import scrape_mars
import pymongo 

app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_data


#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
#mongo = PyMongo(app)

@app.route('/')
def index():
    mars = db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route("/scrape")
def scrap():

    # Run scrapped functions
    mars_info = db.mars.find_one()
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)