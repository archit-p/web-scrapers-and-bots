from selenium import webdriver
import bs4
from Queue import Queue
import time

class scraper():
    #init function
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.city_Q = Queue()
        self.filename = "output.csv"

    #function to get list of cities
    def get_city_details(self):
        url = 'https://geo.craigslist.org/iso/us'
        self.driver.get(url)
        page_html = self.driver.execute_script("return document.body.innerHTML")
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
        return cities

    #helper funciton to write a line to file
    def write_line_to_file(self, line=None):
        fp = open(self.filename, "a+")
        content = fp.read()
        fp.close()
        if line in content:
            print("Duplicate details " + line + ". Not printing to file!")
        else:
            print("Writing " + line + "to file...")
            fp = open(self.filename, "a+")
            fp.write(line + "\n")
            fp.close()

    #function to write email and telephone number to file
    def write_details_to_file(self, tel=None, email=None):
        line = str(tel) + "," + str(email)
        self.write_line_to_file(line)

    #function to select the city based on user input
    def select_city(self):
        cities = self.get_city_details()
        get_city = raw_input("Which city do you want to search? (Enter 'all' for all cities)\n---->")
        if get_city == "all":
            for city in cities:
                self.city_Q.put(city)
        else:
            for city in cities:
                if get_city in city['name']:
                    self.city_Q.put(city)

    #function to handle a single page and return the ad urls found
    def handle_page(self, city):
        print("Going to the city page")
        lostfoundurl = city['link'] + '/search/laf'
        self.driver.get(lostfoundurl)
        totalcount = self.driver.find_element_by_class_name('totalcount').text
        innerHTML = self.driver.execute_script("return document.body.innerHTML")
        newsoup = bs4.BeautifulSoup(innerHTML, "lxml")
        lost_list = newsoup.find("ul", class_="rows")
        lost_list = lost_list.find_all("a", class_="result-title")
        if(len(lost_list) > int(totalcount)):
            lost_list = lost_list[:int(totalcount)-1]
        elif(len(lost_list) < int(totalcount)):
            while(len(lost_list) < int((totalcount))):
                next_button = self.driver.find_element_by_class_name("next")
                next_button.click()
                innerHTML = self.driver.execute_script("return document.body.innerHTML")
                newsoup = bs4.BeautifulSoup(innerHTML, "lxml")
                new_lost_list = newsoup.find("ul", class_="rows")
                new_lost_list = new_lost_list.find_all("a", class_="result-title")
                lost_list += new_lost_list

        page_urls = list()
        for lost in lost_list:
            if(lost['href'] != '#'):
                page_urls.append(lost['href'])

        print("Found " + totalcount + "lost and found ad links")
        return page_urls

    #function to iterate through each page
    def handle_pages(self):
        self.select_city()
        while not self.city_Q.empty():
            city = self.city_Q.get()
            page_urls = self.handle_page(city)
            self.scrape(page_urls)

    #function to get phone numbers from range of urls
    def scrape(self,page_urls):
        for page_url in page_urls:
            self.driver.get(page_url)
            button = self.driver.find_element_by_class_name("reply_button")
            button.click()
            time.sleep(10)
            try:
                tel = self.driver.find_element_by_class_name("reply-tel-number").text
                tel = tel.encode('utf8')
                tel = tel[4:]
                tel = tel.strip()
            except:
                tel = str(None)
            try:
                email = self.driver.find_element_by_class_name("mailapp").text
                email = email.encode('utf8')
                email = email.strip()
            except:
                email = None
            self.write_details_to_file(tel, email)

s = scraper()
s.handle_pages()
