from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests, sys, io, re
import pandas as pd

def get_latest_news():
    mars_data = {}
    nasa_news_url="https://mars.nasa.gov/news/"
    browser = Browser('chrome', headless=True)
    browser.visit(nasa_news_url)
    html = browser.html
    soup=bs(html,'lxml')
    latest_list_item = soup.find("div", class_="list_text")
    mars_data["latest_news_title"] = latest_list_item.find("div", class_="content_title").text
    mars_data["latest_news_body"] = latest_list_item.find("div", class_="article_teaser_body").text
    #mars_data["latest_image_url"] = get_latest_featured_image()
    browser.quit()

    return mars_data

def get_latest_featured_image():
    ## https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    image_details={}
    base_url= "https://www.jpl.nasa.gov"
    mars_images_link = f"{base_url}/spaceimages/?search=&category=Mars"

    browser = Browser('chrome', headless=True)
    browser.visit(mars_images_link)

    html = browser.html
    soup=bs(html,'lxml')

    result = soup.find("footer")
    relative_img_url=result.find("a")["data-link"]

    data_link = f"{base_url}{relative_img_url}"
    browser.visit(data_link)
    html = browser.html
    soup = bs(html, 'lxml')
    hires_image_url=soup.find("article").find("figure", class_="lede").find("a")["href"]

    #featured_image_url = f"{base_url}{hires_image_url}"
    browser.quit()
    image_details["image_url"] = f"{base_url}{hires_image_url}"
    return image_details

def get_weather_details():
    mars_weather_dict={}
    twitter_link = "https://twitter.com/marswxreport?lang=en"

    response = requests.get(twitter_link)
    #print("Twitter Link => "+response)

    soup = bs(response.text, 'lxml')
    
    results = soup.find_all('div', class_="content")
    mars_weather=""

    for result in results:
        tweet_text = result.find("p", class_ = "tweet-text")
        tweet_link = result.find("a", class_ = "twitter-timeline-link")
        tweet_date = result.find("span", class_ = "_timestamp")
        if "InSight sol" in result.text:
            #print("~" * 100)
            if tweet_link:
                #print(f"[{tweet_date.text}] => {tweet_text.text} \n{tweet_link.text}")
                #print("Modified String")
                #print(tweet_text.text.replace(tweet_link.text,""))
                mars_weather=tweet_text.text.replace(tweet_link.text,"")
                #print(mars_weather)
                break
            else:
                #print(f"[{tweet_date.text}] => {tweet_text.text}")
                mars_weather = tweet_text.text
                break
    mars_weather_dict["weather_data"] = mars_weather
    return mars_weather_dict

def get_mars_facts():
    mars_facts_dict = {}
    mars_facts_url = "https://space-facts.com/mars/"

    tables = pd.read_html(mars_facts_url)

    df=tables[1]
    df.rename(columns={0:"Description", 1:"Value"}, inplace = True)
    df.set_index('Description', inplace= True)
    mars_facts_dict["facts"] = df.to_html(classes = "table table-bordered table-striped")

    return mars_facts_dict

