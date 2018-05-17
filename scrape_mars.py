
# coding: utf-8

# In[116]:


from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import pandas as pd
import time


# **Collecting Mars news**

# In[2]:


get_ipython().system('which chromedriver')


# In[3]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


url = 'https://mars.nasa.gov/news/'


# In[5]:


browser.visit(url)


# In[6]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[7]:


news_title = soup.find('ul', class_='item_list ').find('li', class_='slide').find('div', class_='content_title').find('a').text


# In[8]:


news_p = soup.find('ul', class_='item_list ').find('li', class_='slide').find('div', class_='article_teaser_body').text


# In[10]:


print(news_title)
print(news_p)


# **Getting Mars image link**

# In[11]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


# In[12]:


browser.visit(url)


# ***Open full image***

# In[13]:


browser.find_by_css('div[class="default floating_text_area ms-layer"]').find_by_css('footer').find_by_css('a[class="button fancybox"]').click()


# ***Open More Info***

# In[14]:


browser.find_by_css('div[id="fancybox-lock"]').find_by_css('div[class="buttons"]').find_by_css('a[class="button"]').click()


# In[15]:


featured_image_url = browser.find_by_css('div[id="page"]').find_by_css('section[class="content_page module"]').find_by_css('figure[class="lede"]').find_by_css('a')['href']


# In[16]:


print(featured_image_url)


# **Scraping Mars weather**

# In[17]:


url = 'https://twitter.com/marswxreport?lang=en'


# In[18]:


browser.visit(url)


# In[37]:


# all_tweets = browser.find_by_css('ol[id="stream-items-id"]')


# In[39]:


tweet_features = 'Sol' and 'high' and 'low' and 'pressure' and 'hPa' and 'daylight'


# In[42]:


for tweet in browser.find_by_css('ol[id="stream-items-id"]'):
    if tweet_features in browser.find_by_css('div[class="js-tweet-text-container"]')    .find_by_css('p').text:
        mars_weather = browser.find_by_css('div[class="js-tweet-text-container"]')        .find_by_css('p').text
        break


# In[44]:


print(mars_weather)


# **Gathering Mars facts**

# In[76]:


url = 'http://space-facts.com/mars/'


# In[77]:


tables = pd.read_html(url)


# In[78]:


df = tables[0]
df.columns = ['Parameter', 'Value']
df = df.set_index('Parameter')
df


# In[79]:


html_table = df.to_html()
html_table


# **Hemispheres data**

# In[81]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# In[104]:


browser.visit(url)


# In[139]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[163]:


spheres = soup.find('div', class_='collapsible results').find_all('div', class_='item')


# In[164]:


hemisphere_image_urls = []
for x in range(len(spheres)):
    title = spheres[x].find('div', class_="description").find('h3').text
    browser.find_by_css('div[class="collapsible results"]').find_by_css('div[class="item"]')[x]    .find_by_css('div[class="description"]').find_by_css('a').click()
    for img in browser.find_by_css('div[class="downloads"]').find_by_css('a'):
        if ('Original' in img.text):
            img_url = img['href']
#         if ('Sample') in img.text:
#             img_url = img['href']
    browser.click_link_by_partial_text('Back')
    dic = {'title': title, 'img_ulr': img_url}
    hemisphere_image_urls.append(dic)
    time.sleep(3)
    print(title)
    print(img_url)


# In[165]:


hemisphere_image_urls

