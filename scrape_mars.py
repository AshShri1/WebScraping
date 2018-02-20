
# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
import time
from splinter import Browser
import requests as req
import html5lib



def scrape():

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'



    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')



    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="rollover_description_inner").text


    browser = Browser('chrome', headless=False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)



    html = browser.html
    soup = BeautifulSoup(html, "html.parser")



    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)

    browser.click_link_by_partial_text('more info')


    new_html = browser.html
    new_soup = BeautifulSoup(new_html, 'html.parser')
    image_url = new_soup.find('img', class_='main_image')
    partial_image_url = image_url.get('src')

    print(partial_image_url)

    recent_mars_image_url = "https://www.jpl.nasa.gov" + partial_image_url

    print(recent_mars_image_url)


    #get mars weather
    twitter_response = req.get("https://twitter.com/marswxreport?lang=en")
    twitter_soup = BeautifulSoup(twitter_response.text, 'html.parser')


    tweet_containers = twitter_soup.find_all('div', class_="js-tweet-text-container")


    print(tweet_containers[0].text)
    p = tweet_containers[0].text
    type(p)


    for tweets in tweet_containers:
        if tweets.text:
            print(tweets.text)
            break


    for i in range(10):
        tweets = tweet_containers[i].text
        if "Sol " in tweets:
            print(tweets)
            MarsWeather = tweets
            break


    #Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc. Use Pandas to convert the data to a HTML table string. 

    MarsSpace_Facts = req.get("https://space-facts.com/mars/")



    MarsSpace_df = pd.read_html(MarsSpace_Facts.text)[0]


    MarsSpace_df.set_index(0, inplace=True)


    MarsSpace_df



    MarsSpace_html = MarsSpace_df.to_html()
    MarsSpace_html
    MarsSpace_html.replace('\n', '')



    #Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

    USGSArch_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    USGSArch_request = req.get(USGSArch_URL)



    soup = BeautifulSoup(USGSArch_request.text, "html.parser")
    hemisphere_attr_list = soup.find_all('a', class_="itemLink product-item")



    hemisphere_image_url = []
    for hemisphere_image in hemisphere_attr_list:
        hemisphere_image_title = hemisphere_image.find('h3').text
        hemisphere_image_link = "https://astrogeology.usgs.gov/" + hemisphere_image['href']
        hemisphere_image = req.get(hemisphere_image_link)
        soup = BeautifulSoup(hemisphere_image.text, 'lxml')
        hemisphere_image_tag = soup.find('div', class_='downloads')
        image_url = hemisphere_image_tag.find('a')['href']
        hemisphere_image_url.append({"Title": hemisphere_image_title, "Image_Url": image_url})



    hemisphere_image_url


    Mars_Data = {
         "News_Title": news_title,
         "News_Paragraph": news_paragraph,
         "Most_Recent_Mars_Image": recent_mars_image_url,
         "Mars_Weather": MarsWeather,
         "Mars_URL": hemisphere_image_url
         }



    return(Mars_Data)


# In[ ]:



