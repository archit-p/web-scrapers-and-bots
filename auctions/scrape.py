from selenium import webdriver
import time
import bs4

class scraper:
    def __init__(self):
        # url to the page
        # change this to scrape a different page
        self.url = 'https://okaloosa.realtaxdeed.com/index.cfm?zaction=AUCTION&Zmethod=PREVIEW&AUCTIONDATE=03/13/2018'
        # filename to save the auction details
        self.filename = 'auction.csv'
        fp = open(self.filename, 'w')
        fp.close()

        # browser instance to use for saving the details
        self.browser = webdriver.Firefox()

    def get_details(self, items):
        itemcount = 0
        for item in items:
            labels = item.select('.AD_LBL')
            data = item.select('.AD_DTA')
            i = 0
            if(itemcount == 0):
                for i in range(len(labels)):
                    fp = open(self.filename, 'a+')
                    if(labels[i].get_text() != ''):
                        fp.write(labels[i].get_text().encode('utf8').replace(',', ',').replace(':', '') + ',')
                    if(i == (len(labels)-1)):
                        fp.write('\n')
                    fp.close()

            i = 0
            while(i < len(labels)):
                fp = open(self.filename, 'a+')
                if(i+1 < len(labels) and labels[i+1].get_text() == ''):
                    fp.write(data[i].get_text().encode('utf8').replace(',' , '.') + ' ' + data[i+1].get_text().encode('utf8').replace(',','.'))
                    i += 1
                else:
                    fp.write(data[i].get_text().encode('utf8').replace(',' , '.'))

                if(i == (len(labels)-1)):
                    fp.write('\n')
                else:
                    fp.write(',')
                i += 1
                fp.close()
            itemcount += 1

    # get the page and create blocks of auction details for running, waiting and closed
    def get_page(self):
        print('Opening the page in a new browser window')
        self.browser.get(self.url)
        res = self.browser.execute_script('return document.body.innerHTML')
        soup = bs4.BeautifulSoup(res, 'lxml')
        running = str(soup.select('#Area_R'))
        runningb = None
        runninglength = 1
        waiting = str(soup.select('#Area_W'))
        waitingb = self.browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[3]/div[3]/div[6]/span[3]/img')
	waitinglength = int(self.browser.find_element_by_xpath('//*[@id="maxWB"]').text)
        i = 0
        if(waitinglength > 1):
            waitinglength -= 1
            for i in range(waitinglength):
                try:
                    waitingb.click()
                    time.sleep(2)
                    res = self.browser.execute_script('return document.body.innerHTML')
                    soup = bs4.BeautifulSoup(res, 'lxml')
                    waiting = waiting + str(soup.select('#Area_W'))
                except:
                    break
                i += 1

        closed = str(soup.select('#Area_C'))
        closedb = self.browser.find_element_by_xpath('/html/body/table/tbody/tr/td[2]/div[3]/div[4]/div[6]/span[3]/img')
        closedlength = int(self.browser.find_element_by_xpath('//*[@id="maxCB"]').text)

	i = 0
        if(closedlength > 1):
            closedlength -= 1
            for i in range(closedlength):
                try:
                    closedb.click()
                    res = self.browser.execute_script('return document.body.innerHTML')
                    soup = bs4.BeautifulSoup(res, 'lxml')
                    closed = closed + str(soup.select('#Area_C'))
                except:
                    break
                i += 1
        fp = open(self.filename, 'a+')
        fp.write('Running Auctions\n')
        fp.close()
	self.scrape(running)
        print('\nWritten details for running auctions into the file\n\n')
        fp = open(self.filename, 'a+')
        fp.write('Waiting Auctions\n')
        fp.close()
	self.scrape(waiting)
        print('\nWriting details for waiting auctions into the file\n\n')
        fp = open(self.filename, 'a+')
        fp.write('Closed Auctions\n')
        fp.close()
        self.scrape(closed)
        print('\nWriting details for closed auctions into the file\n\n')
        self.browser.close()
        print('Finished all categories! Exiting!')
	
    # scrape each block
    def scrape(self, block):
        soup = bs4.BeautifulSoup(block, 'lxml')
        items = soup.select('.AUCTION_ITEM')
        self.get_details(items)

s = scraper()
s.get_page()
