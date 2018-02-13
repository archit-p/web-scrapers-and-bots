from selenium import webdriver
import time as tm
from lxml import html
from selhelper import headless

class scraper:
    def __init__(self):
        self.url = "http://cryptopanic.com/news"
        self.filename = "output.csv"
        self.baseurl = "http://cryptopanic.com"

    def new_browser(self):
        options = headless.setup_headless()
        browser = webdriver.Firefox(firefox_options=options)
        browser.set_window_size(400, 800)
        return browser

    def touch_file(self):
        print("Creating new file " + self.filename)
        fd = open(self.filename, "w")
        fd.write("Time,Title,Positive,Negative,Important,Save\n")
        fd.close()

    def load_view_more(self, browser):
        print("waiting for response from page...")
        browser.get(self.url)
        tm.sleep(10)
        elem = browser.find_element_by_class_name("btn")
        elem.click()
        # load the page until no more elements are left
        while(elem != []):
            try:
                elem = browser.find_element_by_class_name('btn')
                tm.sleep(5)
                elem.click()
                print("loading elements...")
            except:
                break
        innerHTML = browser.execute_script("return document.body.innerHTML")
        htmlElem = html.document_fromstring(innerHTML)
        return htmlElem

    def scrape(self, browser, htmlElem):
        # main scraping logic, find the elements and write them to a csv file
        newsrows = htmlElem.cssselect(".news-row")
        i = 0
        for newsrow in newsrows:
            print("Working on " + str(newsrow))
            positive = newsrow.cssselect(".action-positive .num")
            negative = newsrow.cssselect(".action-negative .num")
            important = newsrow.cssselect(".action-important .num")
            save = newsrow.cssselect(".action-save .num")
            timedate = newsrow.cssselect(".nc-date time")
            link = self.baseurl + newsrow.cssselect("a.news-cell")[0].get('href')
            
            print("Visiting " + link + " to get title...")
            browser.get(link)
            tm.sleep(5)
            innerHTML = browser.execute_script("return document.body.innerHTML")
            htmlElem = html.document_fromstring(innerHTML)
            heading = htmlElem.cssselect(".post-title span")[0].text_content().strip()
    
            print(heading)
            print(timedate)
            print(save)
            print(important)
            print(positive)
            print(negative)
    
            if(heading != ""):
                heading ='"' + heading.strip() + '"'
            else:
                heading = ""
                
            if(positive != []):
                positive = positive[0].text_content()
            else:
                positive = "0"

            if(negative != []):
                negative = negative[0].text_content()
            else:
                negative = "0"

            if(important != []):
                important = important[0].text_content()
            else:
                important = "0"

            if(save != []):
                save = save[0].text_content()
            else:
                save = "0"

            if(timedate != []):
                timedate = timedate[0].text_content()
            else:
                timedate = "0h"

            if(i != 0):
                print("Writing to file")
                fd = open(self.filename, "a+")
                fd.write(timedate.encode("utf8") + "," + heading.strip().encode('utf8') + "," + positive.encode('utf8') + "," + negative.encode("utf8") + "," + important.encode("utf8") + "," + save.encode("utf8") + "," + "\n")
                fd.close()
            i += 1

    
def main():
    s = scraper()
    browser = s.new_browser()
    s.touch_file()
    browser.get(s.url)
    htmlElem = s.load_view_more(browser)
    s.scrape(browser, htmlElem)

if __name__ == "__main__":
    main()
