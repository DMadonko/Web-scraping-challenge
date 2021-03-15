# --- dependencies and setup ---
import pandas as pd
from splinter import Browser
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def init_browser():
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # ******************************************************************************************************************************
    # Scraping Mars News
    # *****************************************************************************************************************************
    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    print("Scraping Mars News...")

    html = browser.html

    #HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    #get the first <li> item under <ul> list of headlines
    first_li = soup.find('li', class_='slide')

    #save the news title
    title = first_li.find('div', class_='content_title').text

    #save the news paragraph
    para = first_li.find('div', class_='article_teaser_body').text

    print("Mars News: Scraping Complete!")

    # *****************************************************************************************************************************
    # Scraping JPL Featured Image URL 
    # *****************************************************************************************************************************
    
    #visit the JPL Featured Space Image website
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    main_url = "https://www.jpl.nasa.gov"
    browser.visit(featured_image_url)
    time.sleep(2)

    #create HTML object
    html = browser.html

    #parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    #Retrieve background-image url from style tag 
    image_url=soup.find_all('article')
    image_url  = soup.find('article')['style']

    image_url=image_url.split("'")[1]

    #Concatenate website url with scrapped route
    feat_image_url= main_url+image_url
    feat_image_url
  

    print("JPL Featured Space Image: Scraping Complete!")

    # *****************************************************************************************************************************
    #  Scraping Mars Facts
    # *****************************************************************************************************************************
    
    #Mars Facts website
    MarsFacts_url = 'https://space-facts.com/mars/'
    browser.visit(MarsFacts_url)
    time.sleep(2)

    #HTML object
    html = browser.html

    table = pd.read_html(html)

    facts_df = table[0]
    acts_df.columns =['Description', 'Value']
    facts_df

    facts_df.to_html('marsfacts.html', index=False)

    print("Mars Facts: Scraping Complete!")

    # *****************************************************************************************************************************
    #  Scraping Mars Hemisphere images
    # *****************************************************************************************************************************
    MarsHemImage_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(MarsHemImage_url)
    time.sleep(2)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_divs = soup.find_all('div', class_="item")

    hemisphere_image_data = []


    for hemisphere in range(len(hemisphere_divs)):

        hem_link = browser.find_by_css("a.product-item h3")
        hem_link[hemisphere].click()
        time.sleep(1)
    
        img_detail_html = browser.html
        imagesoup = BeautifulSoup(img_detail_html, 'html.parser')
    
        base_url = 'https://astrogeology.usgs.gov'
    
        hem_url = imagesoup.find('img', class_="wide-image")['src']
    
   
        img_url = base_url + hem_url

  
        img_title = browser.find_by_css('.title').text
    
   
        hemisphere_image_data.append({"title": img_title,
                              "img_url": img_url})
    
        browser.back()
      
    browser.quit()

    hemisphere_image_data


    print("Mars Hemisphere Images: Scraping Complete!")
    
    # *****************************************************************************************************************************
    #  Store all values in dictionary
    # *****************************************************************************************************************************

    scraped_data = {
        "title": title,
        "para": para,
        "featured_image_url": featured_image_url,
        "mars_fact_table": html_table, 
        "hemisphere_images": hemisphere_image_data
    }

    # --- Return results ---
    return scraped_data