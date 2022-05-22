#!/usr/bin/env python
# coding: utf-8

# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# set up executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

#optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

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

# # Image Scraping
# ### Featured Images

# setting up the visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# # Mars Facts

import pandas as pd

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# convert df to html format
df.to_html()

# # Challenge

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# Parse HTML with soup
html = browser.html
hemisphere_soup = soup(html, 'html.parser')


# 2. Create a list to hold dictionary of the images and titles.(link:title)
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(4):

    # empty dictionary to hold key value pairs (link: title)
    link_title = {}

    # find clickable, and then click
    click_this = browser.find_by_tag("h3")[i]
    click_this.click()

    # html parser
    html = browser.html
    scrape_soup = soup(html, 'html.parser')
    scrape_img_link = scrape_soup.select_one('div.downloads')
    scrape_title = scrape_soup.select_one('div.content')

    # store scrapes in variables
    image_link = scrape_img_link.find('a', href=True).get('href')
    title = scrape_title.find('h2', class_='title').get_text()

    # append to dictionary
    link_title[title] = image_link

    # append dictionaries to list
    hemisphere_image_urls.append(link_title)
    
    # go back
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

