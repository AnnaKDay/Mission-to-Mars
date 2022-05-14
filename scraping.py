#!/usr/bin/env python
# coding: utf-8

# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

# scraping function
def scrape_all():
    # set up executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # set news title and paragraphs variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dict
    data = {'news_title': news_title, 'news_paragraph': news_paragraph, 'featured image': featured_image(browser),
            'facts': mars_facts(), 'last_modified': dt.datetime.now()}
    
    # stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    #optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # add try except for error handling
    try:
        # set up HTML parser
        html = browser.html
        news_soup = soup(html, 'html.parser')
        slide_elem = news_soup.select_one('div.list_text')


        # scraping for the title of the first article displayed on page
        slide_elem.find('div', class_='content_title')

        # use the parent element to find the first 'a' tag and save as 'news_title'
        # will return a different, updated article as the website is updated
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        news_teaser = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_teaser
    except AttributeError:
        return None, None

    return news_title, news_teaser
#  Image Scraping
#  Featured Images

# featured image function
def featured_image(browser):
    # setting up the visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    #browser.is_element_present_by_css('div.list_text', wait_time=1)
    # cant connect to server, will not troubleshoot and solve right now
    # will ask dad to help understand what this means

    try:

        # Find and click the full image button
        full_image_elem = browser.find_by_tag('button')[1]
        full_image_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

# Mars Facts


import pandas as pd

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #return df

    # convert df to html format
    return df.to_html()

if __name__ == '__main__':
    print(scrape_all())





