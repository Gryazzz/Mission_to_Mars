

def scrape_mars():
    from bs4 import BeautifulSoup
    from splinter import Browser
    import pandas as pd
    from selenium import webdriver
    import time

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False, incognito=True)

    # scraping news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('ul', class_='item_list ').find('li', class_='slide').find('div', class_='content_title')\
    .find('a').get_text()

    news_p = soup.find('ul', class_='item_list ').find('li', class_='slide')\
    .find('div', class_='article_teaser_body').get_text()

    # print(news_title)
    # print(news_p)

    # scraping weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(3)

    tweet_features = 'Sol' and 'high' and 'low' and 'pressure' and 'hPa' and 'daylight'
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    for tweet in soup.find_all('li', class_="js-stream-item stream-item stream-item "):
        if tweet_features in tweet.find('div', class_='js-tweet-text-container').find('p').text:
            mars_weather = tweet.find('div', class_='js-tweet-text-container').find('p').text
            break
    
    print(mars_weather)

    # scraping featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)

    browser.find_by_css('div[class="default floating_text_area ms-layer"]').find_by_css('footer')\
    .find_by_css('a[class="button fancybox"]').click()
    time.sleep(3)

    browser.find_by_css('div[id="fancybox-lock"]').find_by_css('div[class="buttons"]')\
    .find_by_css('a[class="button"]').click()

    featured_image_url = browser.find_by_css('div[id="page"]').find_by_css('section[class="content_page module"]')\
    .find_by_css('figure[class="lede"]').find_by_css('a')['href']

    # print(featured_image_url)

    #scraping facts
    url = 'http://space-facts.com/mars/'

    tables = pd.read_html(url)

    df = tables[0]
    df.columns = ['Description', 'Value']
    df = df.set_index('Description')

    facts_table = df.to_html()
    # print(facts_table)

    #scraping hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    spheres = soup.find('div', class_='collapsible results').find_all('div', class_='item')

    hemisphere_image_urls = []

    for x in range(len(spheres)):
        title = spheres[x].find('div', class_="description").find('h3').text

        browser.find_by_css('div[class="collapsible results"]').find_by_css('div[class="item"]')[x]\
        .find_by_css('div[class="description"]').find_by_css('a').click()

        for img in browser.find_by_css('div[class="downloads"]').find_by_css('a'):
            # if ('Original' in img.text):
            #     img_url = img['href']
            if ('Sample') in img.text:
                img_url = img['href']

        browser.click_link_by_partial_text('Back')

        dic = {'title': title, 'img_url': img_url}
        hemisphere_image_urls.append(dic)
        
        time.sleep(3)
        
    # print(hemisphere_image_urls)

    scrape_dic = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'weather': mars_weather,
        'image': featured_image_url,
        'facts_table': facts_table,
        'hemispheres': hemisphere_image_urls
    }  
    print('scrape dictionary is ready')

    browser.quit()
    return scrape_dic

