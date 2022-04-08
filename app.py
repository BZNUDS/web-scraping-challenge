from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask to establish Mongo connection
app.config["MONGO_URI"] ="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)   

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    try:
        mars = mongo.db.mars.find_one()
    except Exception as e:
        print()
        print(f'error: {e}')
        print()

    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars = mongo.db.mars
    # Run the scrape function (was mars_news but now scrape_all)
    mars_data = scrape_mars.scrape_all()
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print(f'Printing mars_data while in /scape: {mars_data}')
    print()


    # Update the Mongo database using update and upsert=True
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run()
