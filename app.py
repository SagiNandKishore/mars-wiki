from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_data

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_news.find_one()
    #featured_image = mongo.db.mars_featured_image.find_one()
    #mars_weather=mongo.db.mars_weather.find_one()
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_news = scrape_mars_data.get_latest_news()
    #featured_image_url= scrape_mars_data.get_latest_featured_image()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.mars_news.update({}, mars_news, upsert=True)
    #mongo.db.mars_featured_image.update({}, featured_image_url, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)