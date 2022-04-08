from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print("Entered app.py")
print()

# Create an instance of Flask
app = Flask(__name__)

# Use flask to establish Mongo connection
app.config["MONGO_URI"] ="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# # Initialize PyMongo to work with MongoDBs
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)

# # Define database and collection 
# # db = client.mars_news_db
# db = client.mars
# collection = db.articles
# print(f'collection; {collection}')      

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('Entering index')
    print()
    # Find one record of data from the mongo database
    try:
        mars = mongo.db.mars.find_one()
    except Exception as e:
        print()
        print(f'error: {e}')
        print()

    print()
    print(f'$$$$$$$$$$$mars in def index aka slash route: {mars}')
    print()

    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('Entering /scrape')
    print()

    mars = mongo.db.mars
    # Run the scrape function (was mars_news but now scrape_all)
    mars_data = scrape_mars.scrape_all()
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print(f'Printing mars_data...was mars_news but now scrape_all: {mars_data}')
    print()


    # Update the Mongo database using update and upsert=True
    print('$$$$$$$$$$$$$$$$$$$$$$$ ready to perform mars.update_one')
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    print('$$$$$$$$$$$$$$$$$$$$$$$ did it perform mars.update_one????')
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run()
