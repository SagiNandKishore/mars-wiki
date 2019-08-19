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
    mars_data["latest_image_url"] = get_latest_featured_image()
    browser.quit()

    return mars_data

def get_latest_featured_image():
    ## https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
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

    featured_image_url = f"{base_url}{hires_image_url}"
    browser.quit()

    return featured_image_url