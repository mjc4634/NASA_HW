


from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# In[2]:
def scrape(): 
    try:
        browser = init_browser()

        # * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
        #url of page to be scraped
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)


        # In[3]:


        # retrieve page with browser module
        html = browser.html


        # In[4]:


        soup = BeautifulSoup(html, 'html.parser')


        # In[5]:


        #print(soup.prettify())


        # In[6]:


        title = soup.find('div', class_="content_title")
        paragraph = soup.find('div', class_="article_teaser_body")


        # In[7]:


        news_title = title.text


        # In[8]:


        news_p = paragraph.text
        print(news_title)
        print(news_p)


        # In[9]:


        # news_dict = {}
        # for i in range(len(title)):
        #     key = title[i].find('a').text.strip()
        #     value = paragraph[i].text.strip()
        #     news_dict[i] = {key:value}
        #     #print(key, value)


        # In[16]:


        # Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

        # * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
        base_url = 'https://www.jpl.nasa.gov'
        mars_img_url = base_url + '/spaceimages/?search=&category=Mars'
        browser.visit(mars_img_url)
        browser.is_text_present('Full IMAGE')
        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(2)

        img_html = browser.html
        img_soup = BeautifulSoup(img_html, 'html.parser')
        
        img_url = img_soup.find('div', class_='fancybox-inner').img['src']
        print(img_url)
        featured_image_url = base_url + img_url
        print(featured_image_url)
        


        # In[22]:


        # ### Mars Weather

        # * Visit the Mars Weather twitter account [here]
        # (https://twitter.com/marswxreport?lang=en) and scrape the latest
        # Mars weather tweet from the page. Save the tweet text for the weather 
        # report as a variable called `mars_weather`.


        # In[33]:


      

        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)


        # In[34]:


        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')


        # In[35]:


        tweet = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')


        # In[36]:


        mars_weather = tweet.text.split("pic")[0]


        # In[37]:


        ### Mars Facts
        # Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the 
        # table containing facts about the planet including Diameter, Mass, etc.
        # Use Pandas to convert the data to a HTML table string.


        # In[67]:


        

        url = 'https://space-facts.com/mars/'
        browser.visit(url)


        # In[68]:


        html = browser.html
        table = pd.read_html(url)[0]
        table.columns = ['Names', 'Value']
        table = table.to_html(index=False, justify='center')
        time.sleep(2)


        # In[69]:


        ### Mars Hemispheres

        # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
        # to obtain high resolution images for each of Mar's hemispheres.

        # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

        # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
        # Use a Python dictionary to store the data using the keys `img_url` and `title`.

        # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


        # In[70]:


        

        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)


        # In[71]:


        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')


        # In[72]:


        hemi_soup = soup.find_all('a', class_='itemLink product-item')


        # In[74]:


        ### get hemi image pages
        home_url = 'https://astrogeology.usgs.gov'
        hemisphere_image_list = []
        title_list = []
        for hemi in hemi_soup:
            href = hemi['href']
            title = hemi.text
            title_list.append(title)
            full_page_url = home_url + href
            hemisphere_image_list.append(full_page_url)
        hemisphere_images = list(dict.fromkeys(hemisphere_image_list))
        title_list = list(filter(None, list(dict.fromkeys(title_list))))


        # In[75]:


        jpg_list = []
        for url in hemisphere_images:
            
            browser.visit(url)
            html = browser.html
            new_soup = BeautifulSoup(html, 'html.parser')
            src = new_soup.find('img', class_='wide-image')['src']
            full_url = home_url + src
            jpg_list.append(full_url)


        # In[115]:


        hemisphere_image_urls = []
        image_urls = {}
        for i in range(len(jpg_list)):
            image_urls = {'title': title_list[i], 'img_url': jpg_list[i]}
            hemisphere_image_urls.append(image_urls)


        # In[116]:


        hemisphere_image_urls


        # In[ ]:
        mars_data = {
        "News_Title": news_title,
        "Paragraph_Text": news_p,
        "Most_Recent_Mars_Image": featured_image_url,
        "Mars_Facts": table,
        "Mars_Weather": mars_weather,
        "mars_h": hemisphere_image_urls
            }
        return mars_data

    finally:
        browser.quit()




# In[ ]:

# debugging using the following lines
if __name__ == "__main__":
    listings = scrape()
    print(listings)


