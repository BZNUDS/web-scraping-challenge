# Converted my Jupyter Notebook mission_to_mars.ipynb into to scrape_mars.py
# then bloked off key funtions 
# Dependencies
# Started with scrape_costa.py basics and added more over time

from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager

import requests
import pymongo
import os
import pandas as pd

print("Entered scrape_mars.py")

# Set-up path and browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path, headless=False)

# # Initialize PyMongo to work with MongoDBs
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)

# # Define database and collection  from Eli's Stu_Reddit_Scraper for 12.2.4 that he slacked to us at 7:51 on 3/16
# db = client.mars_news_db
# collection = db.articles
# print(f'collection; {collection}')


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_mars_image(browser):
    # Step 1 - Scraping:  JPL Mars Space Images - Featured Mars Image

    # Set-up path and browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    url = 'https://spaceimages-mars.com/'

    # Retrieve page with the visit module
    browser.visit(url)
    html = browser.html

    try: 
        # Click on "FULL IMAGE" button
        browser.links.find_by_partial_text('FULL IMAGE').click()

        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.prettify())

        # Find full size image
        fade_in_image = soup.find_all("img", "headerimage fade-in")
        featured_image_url=url + fade_in_image[0]['src']
        print(f'featured_image_url: {featured_image_url}')
        print()
        browser.quit()
        return featured_image_url

    except Exception as e:
        print(f'error: {e}')
        browser.quit()
        return None


def mars_facts(browser):
        
    # Step 1 - Scraping:  JPL Mars Space Images - Mars Facts

    # Set-up path and browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    url = 'https://galaxyfacts-mars.com/'

    try:
        tables = pd.read_html(url)
        # Get Dataframe of first table
        df = tables[0]
        print(df.head())

        # Convert df to html
        html_table = df.to_html()
        browser.quit()
        print(f'html_table: {html_table}')
        return df, html_table

    except Exception as e:
        print(f'error: {e}')
        browser.quit()
        return None, None

def mars_hemispheres(browser):

    # Step 1 - Scraping:  Mars Hemispheres

    # Set-up path and browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    url = 'https://marshemispheres.com/'

    # Retrieve page with the visit module
    browser.visit(url)

    html = browser.html
    # print("html")
    # print(html)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    results = soup.find_all('div', class_='item')

    i = 0
    titles = {}
    img_urls = {}
    Enhanced_dict= {}
    mydict ={}
    hemisphere_image_urls = []

    # Next look for <h3>
    for result in results:
        # Error handling
        try:
            # Identify and return title of listing
            title = results[i].find('h3').text
            titles[i]=title
            
            # Run only if title is available
            if (title != ''):
                
                # Click on proper enhanced image button
                browser.links.find_by_partial_text(title).click()
                time.sleep(0.5)

                html = browser.html
                # print(html)

                # Create BeautifulSoup object; parse with 'html.parser'; find description iterables
                enhanced_soup = BeautifulSoup(html, 'html.parser')
                enhanced_results = enhanced_soup.find_all('div', class_='description')

                # Loop through returned results
                for enhanced_result in enhanced_results:
                    # Error handling
                    try:
                        link = enhanced_result.a['href']
    #                     print(link)
                        img_url=url + link
    #                     print(img_url)
                    except Exception as e:
                        print(e)
                
    #             print(f'title: {title}')
    #             print(f'img_url: {img_url}')

        
                #Assigning value to a specific key. This key will be added if its not available already. 
                Enhanced_dict[title] = img_url
                # print(f'Enhanced_dict is now: {Enhanced_dict}')
                
                # Click on back button to return to home page
                browser.links.find_by_partial_text('Back').click()
    #             print("Should sleep for 0.5")
                time.sleep(0.5)
                
        except Exception as e:
            print(f'error: {e}')
            return None
        i+=1

    hemisphere_image_urls = [Enhanced_dict]
    print()
    print(f'hemisphere_image_urls: {hemisphere_image_urls}')
    print()
    browser.quit()
    return hemisphere_image_urls
    