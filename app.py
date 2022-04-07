from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print("Entered app.py")
print()

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('Entering index')
    print()
    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("Templates/index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('Entering /scrape')
    print()
    try:
        mars = mongo.db.mars
        # Run the scrape function
        mars_data = scrape_mars.mars_news()
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print('Printing mars_data: {mars_data}')
        print()
    except Exception as e:
        print()
        print(f'error: {e}')
        print()


    # Update the Mongo database using update and upsert=True
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('Commenting out the mars.update_one line ~50')
    # mars.update_one({}, {"$set": mars_data}, upsert=True)
    

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run()
