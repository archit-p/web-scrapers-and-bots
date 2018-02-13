import requests
from lxml import html
import sys
from urlparse import urlsplit

class scraper:
    # initialize an object with filename and url
	def __init__(self, filename, url):
		self.filename = filename
		self.url = url
		self.baseurl = "https://en.wikipedia.org/"

    #function to create a file
	def touch_file(self):
		fd = open(self.filename, "w")
                fd.write("Airline,Airport,Serves,Nickname\n")
		fd.close()

    #request for the page
	def request(self):
		response = requests.get(self.url)
		htmlResponse = response.content
		htmlElem = html.document_fromstring(htmlResponse)
		return htmlElem

    #main scraping logic
	def scrape(self, htmlElem):
                selfname = htmlElem.cssselect("#firstHeading")
                selfname = selfname[0].text_content()
    
                selfnicks = htmlElem.cssselect("table.infobox span.nickname")
                for nickname in selfnicks:
                    if(len(nickname.text_content()) == 3):
                        selfnick = nickname.text_content()

		tables = htmlElem.cssselect("table.wikitable")
                for table in tables:
                    if "Airlines" in table.text_content():
                        table_cols = table.cssselect("td")
                        num = len(table.cssselect("th"))
                        break

		i = 0
		cities = list()
		airlines = list()
		self.touch_file()
		for i in range(0, len(table_cols)):
			if(i%num == 1):
				cities.append(table_cols[i])
                        elif(i%num == 0):
				airlines.append(table_cols[i])

		for i in range(0, len(airlines)):
			airline = airlines[i].cssselect("a")
			airline = airline[0].text_content()
			print("Working on " + airline)
			city_links = list()
			city_names = list()
			nicks = list()
			links = cities[i].cssselect("a")
			name = ""
			serves = ""
			for link in links:
				city_links.append(link.get("href"))
			for link in city_links:
				response = requests.get(self.baseurl + link[1:])
				htmlResponse = response.content
				htmlElem = html.document_fromstring(htmlResponse)
				try:
					name = htmlElem.cssselect("#firstHeading")
					name = name[0].text_content()
				except:
					continue
                                try:
				    	nicks = htmlElem.cssselect("table.infobox span.nickname")
                                    	for nickname in nicks:
                                        	if(len(nickname.text_content()) == 3):
                                            		nick = nickname.text_content()
				    	infobox = htmlElem.cssselect("table.infobox tr")
				    	for row in infobox:
						if("Serves" in row.text_content()):
					    		try:
					    			serves = row.cssselect("a")[0].text_content()
			                    		except:
								serves = row.cssselect("td")[0].text_content()
				except:
					print("Couldn't find nickname")
				fd = open(self.filename, 'a+')
				fd.write('"' + airline.encode('utf8') + '"' +  "," + '"' +  name.encode('utf8') + '"' + "," + '"' + serves.encode('utf8') + '"' + "," + nick.encode('utf8') + "," + selfname.encode('utf8') + "," + selfnick.encode('utf8') + "\n")
				fd.close()

def main():
    # take input from user
        url = raw_input("Enter the url: ")
        filename = urlsplit(url)[2][6:] + ".csv"
        print(filename)
	s = scraper(filename, url)
	html = s.request()
	s.scrape(html)
        print("Finished scraping successfully!")
if __name__ == "__main__":
	main()
