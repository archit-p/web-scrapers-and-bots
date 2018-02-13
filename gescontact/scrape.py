from selenium import webdriver
from lxml import html
from multiprocessing import Process
import time
from stem import Signal
from stem.control import Controller

def new_identity():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        controller.close()

def install_firefox_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks", PROXY_HOST)
    fp.set_preference("network.proxy.socks_port", int(PROXY_PORT))
    fp.update_preferences()
    return webdriver.Firefox(firefox_profile=fp)

def getLinks(district):
    url = "http://www.gescontact.pt/distrito/" + district

    browser = install_firefox_proxy("127.0.0.1", 9050)

    browser.get(url)
    links = list()
    filename = district + '.csv'
    fd = open(filename, "w")
    fd.close()

    innerHTML = browser.execute_script("return document.body.innerHTML")
    htmlElem = html.document_fromstring(innerHTML)

    hrefs = htmlElem.cssselect('#ajax_pagination_target a')
    for href in hrefs:
        links.append(href.get('href'))

    i = 2

    while(1):
        try:
            elem = browser.find_element_by_link_text(str(i))
            elem.click()
        except:
            break

        innerHTML = browser.execute_script("return document.body.innerHTML")
        htmlElem = html.document_fromstring(innerHTML)
        try:
            hrefs = htmlElem.cssselect('#ajax_pagination_target a')
        except:
            print('Links not found')
            break

        for href in hrefs:
            fd = open(filename, "a+")
            assert fd is not None
            fd.write(href.get('href').encode('utf8') + '\n')
            print(href.get('href'))
            fd.close()

        print(str(len(links)) + " links gathered")
        i += 1
        if(i%5 == 0):
            new_identity()

def test():
    time.sleep(1)

def main():
    processPool = list()
    i = 0
    districts = ['aveiro', 'beja', 'braga', 'braganca', 'castelo_branco']

    while(i < len(districts)):
        if(len(processPool) != 2):
            p = Process(target=getLinks, args=(districts[i],))
            p.start()
            processPool.append(p)
            i += 1

        for process in processPool:
            if(process.is_alive() == False):
                processPool.remove(process)
    
if __name__ == '__main__':
    main()
