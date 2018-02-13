from selenium import webdriver

URL = 'https://www.youtube.com/results?sp=EgIIBA%253D%253D&search_query={}'

keywords = 'what is my name'
keywords.replace(' ', '+')

search_url = URL.format(keywords)

browser = webdriver.Firefox()

browser.get(search_url)

titles = browser.find_elements_by_id('video-title')
for title in titles:
    print(title.get_attribute('href'))

browser.close()
