from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo 
import scrape_mars
import pymongo 

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)



#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
#mongo = PyMongo(app)

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route("/scrape")
def scrape():

    # Run scrapped functions
    mars_info = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)