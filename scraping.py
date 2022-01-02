#import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = img_title(browser)

    #run all scraping functions and store results in a dictionary
    data = {
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image":featured_image(browser),
        "facts":mars_facts(),
        "last_modified":dt.datetime.now(),
        "url_title":hemisphere_image_urls
    }

    #stop webdriver and return data
    browser.quit()
    return data

# #set up splinter
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    #visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    #optional delay of loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = bs(html, 'html.parser')

    #add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # slide_elem.find('div', class_='content_title')

        #use the parent element to find the first 'a' tag and save it as "new_title"
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # news_title

        #use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        # news_p
    except AttributeError:
        return None, None

    return news_title, news_p


# ## JPL Space Images Featured Images

def featured_image(browser):

    #visit url
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    #find and click on the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the resulting html with soup
    html = browser.html
    img_soup = bs(html, 'html.parser')

    #add try/except for error handling
    try:
        #find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel

    except AttributeError:
        return None

    #use the base URL to create an absolute URL
    img_url = f'{url}{img_url_rel}'
    # img_url
    
    return img_url


# ## Mars Facts

def mars_facts():
    #add try/except for error handling
    try:
        #create dataframe with pandas from table on website
        #use 'read_html' to scrape the facts table into a dateframe
        df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    
    except BaseException:
        return None

    #Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    # df

# df2 = pd.read_html('https://galaxyfacts-mars.com/')[1]
# df2.columns=['category', 'data']
# # df2.set_index('description', inplace=True)
# df2

    #convert dataframe to html format, add bootstrap
    return df.to_html(classes="table table-striped")

#function to scrape the hemisphere data
def img_title(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for x in range(4,11,2):
        hemispheres = {}
        elem1 = browser.find_by_tag('a')[x].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        elem2 = soup.find('li')
        rel_img_url = elem2.find('a').get('href')
        img_url=(f'{url}{rel_img_url}')
        title = soup.find('h2', class_='title').text
        hemispheres = {'img_url':img_url, 'title':title}
        hemisphere_image_urls.append(hemispheres)
        browser.back()  

    return hemisphere_image_urls

if __name__ == "__main__":
    
    #if runing as script, print scraped data
    print(scrape_all())

# #end session
# browser.quit()

