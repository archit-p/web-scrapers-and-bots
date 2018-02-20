from selenium import webdriver
import bs4
from Queue import Queue
import time

url = 'https://geo.craigslist.org/iso/us'
Q = Queue()
driver = webdriver.Firefox()
driver.get(url)

page_html = driver.execute_script("return document.body.innerHTML")
soup = bs4.BeautifulSoup(page_html, 'lxml')
city_list = soup.find("ul", class_="geo-site-list")
city_list = city_list.find_all("a")
cities = list()

li = ''

for li in city_list:
    city = {'name':'','link':''}
    city['name'] = li.getText()
    city['link'] = li['href']
    cities.append(city)

get_city = raw_input('Which city do you want to search?')
if get_city == "all":
    for city in cities:
        Q.put(city)
else:
    for city in cities:
        if get_city in city['name']:
            Q.put(city)

#get results from all cities in queue
while not Q.empty():
    city = Q.get()
    lostfoundurl = city['link'] + '/search/laf'
    driver.get(lostfoundurl)
    totalcount = driver.find_element_by_class_name('totalcount').text
    innerHTML = driver.execute_script("return document.body.innerHTML")
    newsoup = bs4.BeautifulSoup(innerHTML, "lxml")
    lost_list = newsoup.find("ul", class_="rows")
    lost_list = lost_list.find_all("a")
    if(len(lost_list) > int(totalcount)):
        lost_list = lost_list[:int(totalcount)-1]
    # add logic for pagination
    page_urls = list()
    for lost in lost_list:
        if(lost['href'] != '#'):
            page_urls.append(lost['href'])

    for page_url in page_urls:
        driver.get(page_url)
        button = driver.find_element_by_class_name("reply_button")
        button.click()
        time.sleep(10)
        try:
            tel = driver.find_element_by_class_name("reply-tel-number").text
            tel = tel.encode('utf8')
            tel = tel[4:]
            tel = tel.strip()
        except:
            tel = str(None)
        try:
            email = driver.find_element_by_class_name("mailapp").text
            email = email.encode('utf8')
            email = email.strip()
        except:
            email = None

        print(tel + " " + email)
