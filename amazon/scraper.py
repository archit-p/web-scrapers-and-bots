# -*- coding: utf-8 -*-
from selenium import webdriver
from lxml import html
import time


class scraper():
    def __init__(self):
        # define all the variables
        self.baseurl = "https://sellercentral.amazon.com/gp/homepage.html"
        self.filename = "output.csv"
        self.browser = webdriver.Firefox()

    def login(self):
        # visit the page
        self.browser.get(self.baseurl)
        time.sleep(90)
        print("Login process completed")
        try:
            messages = self.browser.find_element_by_link_text("Buyer Messages")
            messages.click()
        except:
            print("Coudln't find messages button")
    
        try:
            response = self.browser.find_element_by_link_text("Response Needed")
            response.click()
            time.sleep(2)
        except:
            print("Couldn't find response button")
    
        try:
            all_messages = self.browser.find_element_by_link_text("All Messages")
            all_messages.click()
        except:
            print("Couldn't find all messages button")

    def scrape(self):
        threads = self.browser.find_elements_by_class_name("click-thread")
        print(threads)
        try:
            for thread in threads:
                self.browser.execute_script("return arguments[0].scrollIntoView();", thread)
                thread.click()
        except:
            print("Couldn't click the thread")

        fd = open(self.filename, "a+")
        file_content = fd.read()

        i = 1
        count = 0
        # define pagination
        while(1):
            next_button = self.browser.find_element_by_link_text(str(i))
            if(next_button is None):
                print("Couldn't find button")
                break
            else:
                next_button.click()

            i += 1
            # scraping logic
            uid = self.browser.find_element_by_id("currentThreadIdSelected").get_attribute("value")
            name = self.browser.find_element_by_id("currentThreadSenderNameSelected").get_attribute("value")
            sender = self.browser.find_element_by_id("currentThreadSenderId").get_attribute("value")
            proxy = self.browser.find_element_by_id("currentThreadSenderProxyEmail").get_attribute("value")

            if(name in file_content):
                count += 1
                continue
            else:
                fd = open(self.filename, "a+")
                fd.write(uid + "," + name + "," + sender + "," + proxy + "\n")
                fd.close()

            # if 10 pre-existing names are encountered, the loop is exited
            if(count == 10):
                break
        print("Finished scraping succesfully!")

def main():
    s = scraper();
    print("Scraper Initiated!\nLogin to page")
    s.login()
    print("Starting to paginate through the messages")
    s.scrape()

if(__name__ == "__main__"):
    main()
