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
    featured_image = mongo.db.mars_featured_image.find_one()
    mars_weather=mongo.db.mars_weather_data.find_one()
    mars_facts = mongo.db.mars_facts.find_one()
    hemisphere_links = mongo.db.mars_hemisphere_images.find()
    return render_template("index.html", mars_data=mars_data, featured_image=featured_image, weather_data = mars_weather, mars_facts = mars_facts, hemisphere_links = hemisphere_links)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_news = scrape_mars_data.get_latest_news()
    featured_image_url= scrape_mars_data.get_latest_featured_image()
    weather_data = scrape_mars_data.get_weather_details()
    mars_facts = scrape_mars_data.get_mars_facts()
    images = scrape_mars_data.get_mars_hemisphere_images()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.mars_news.update({}, mars_news, upsert=True)
    mongo.db.mars_featured_image.update({}, featured_image_url, upsert=True)
    mongo.db.mars_weather_data.update({}, weather_data, upsert = True)
    mongo.db.mars_facts.update({}, mars_facts, upsert=True)
    mongo.db.mars_hemisphere_images.remove()
    mongo.db.mars_hemisphere_images.insert_many(images)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)