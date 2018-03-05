import requests
import bs4
from threading import Thread

class DrivingBot(Thread):
    def __init__(self,zipcodes, lock):
        Thread.__init__(self)
        self.zipcodes = zipcodes
        self.details = []
        self.lock = lock

    def url_gen(self,pincode, pagenum):
        baseurl = "http://finddrivinginstructor.direct.gov.uk/DSAFindNearestWebApp/findNearest.form?postcode={}&pageNumber={}"
        URL = baseurl.format(pincode, str(pagenum));
        try:
            res = requests.get(URL);
        except:
            return "NOTHING FOUND"
        if "Error 500" in res.content:
            return "NOTHING FOUND"
        else:
            return res.content

    def scrape(self,content):
        #print(content);
        soup = bs4.BeautifulSoup(content, "lxml");
        result_list = soup.select("#js-live-search-results");
        try:
            drivers = result_list[0].find_all("li");
        except:
            return None;
        details = [];
        for driver in drivers:
            detail = {'name':'','email':'','num':''};
            name_ele = driver.find("h3", class_="instructor-name");
            detail['name'] = name_ele.text;
            email_ele = driver.find("a", class_="email");
            detail['email'] = email_ele['href'].replace("mailto:","");
            number_ele = driver.find("span", class_="phone");
            detail['num'] = number_ele.text;
            details.append(detail)
        return details

    def run(self):
        for zipcode in self.zipcodes:
            i = 1
            det_list = []
            while(1):
                print("Searching page " + str(i) + " for zipcode " + zipcode)
                innerHTML = self.url_gen(zipcode, i);
                if(innerHTML == "NOTHING FOUND"):
                    break;
                det_list = self.scrape(innerHTML);
                if(det_list is None):
                    continue;
                for det in det_list:
                    if det not in self.details:
                        self.details.append(det)
                        self.lock.acquire();
                        fp = open("results.csv", "a+");
                        fp.write(det['name'] + "," + det['email'] + "," + det['num'] + "," + zipcode + "\n");
                        fp.close();
                        self.lock.release();
                i += 1
