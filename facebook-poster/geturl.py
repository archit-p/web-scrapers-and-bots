from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
# logic explaining how links work - 
# 1. Whenever scrape new URLs if URL hasn't been scraped, append it to both history and current file.
# 2. While using a link read from current file and delete after use.

# make the url using the keywords
def setup_headless():
    options = Options()
    options.add_argument("--headless")
    return options

def new_browser():
    options = setup_headless()
    driver = webdriver.Firefox(firefox_options=options)
    return driver

def get_url(baseurl, keywords):
    keywords = keywords.replace(' ', '+')
    url = baseurl.format(keywords)
    return url

# function to read the history file and return history links
def get_history(his_filename):
    hfp = open(his_filename, 'r')
    history = hfp.read()
    hfp.close()
    history = history.split('\n')
    return history

def check_history(his_filename, link):
    history = get_history(his_filename)
    if link in history:
        return True
    else:
        return False

#helper function to write a line to a csv file
def write_line_to_file(filename, line):
    fp = open(filename, 'a+')
    fp.write(line + '\n')
    fp.close()

def get_links(url):
    browser = new_browser()
    browser.get(url)
    titles = browser.find_elements_by_id('video-title')
    links = list()
    for title in titles:
        link = title.get_attribute('href')
        links.append(link)
    browser.close()
    return links

def random_link():
    fp = open('youtube-links.csv', 'r')
    content = fp.read()
    links = content.split('\n')
    i = random.randint(1, len(links))
    link = links[i]
    return link

def main():
    # define all the variables
    baseurl = 'https://www.youtube.com/results?sp=EgIIBA%253D%253D&search_query={}'
    filename = 'youtube-links.csv'
    store_filename = 'youtube-history.csv'

    # get keywords
    keywords = raw_input('Enter keywords to search for:')
    # get url
    print('Preparing url using the keywords')
    time.sleep(2)
    url = get_url(baseurl, keywords)
    print(url)
    # get links
    print('Getting links from YouTube')
    time.sleep(2)
    links = get_links(url)
    print('Got links!')
    for link in links:
        print(link)

    print('Checking for duplicated and printing links to files')
    time.sleep(2)
    for link in links:
        if(link != None):
            if(check_history(store_filename, link) == False):
                print('New link found ' + link)
                # write to history file
                write_line_to_file(store_filename, link)
                # write to current file
                write_line_to_file(filename, link)

if __name__ == '__main__':
	main()
