from selenium import webdriver
import time

class scraper:
    def __init__(self):
        # url to the page
        self.url = 'https://okaloosa.realtaxdeed.com/index.cfm?zaction=AUCTION&Zmethod=PREVIEW&AUCTIONDATE=03/13/2018'
        # filename to save the auction details
        self.filename = 'auction.csv'

        # browser instance to use for saving the details
        self.browser = webdriver.Firefox()

    def scrape(self):
        self.browser.get(self.url)
        bids = self.browser.find_elements_by_class_name('AUCTION_ITEM')
        get_details(bids)
        button = self.browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[3]/div[3]/div[6]/span[3]/img')
        while(1):
            try:
                button.click()
                time.sleep(1)
            except:
                break
            more_bids = self.browser.find_element_by_class_name('AUCTION_ITEM')
        self.browser.close()

    def get_details(self):

s = scraper()
s.scrape()
