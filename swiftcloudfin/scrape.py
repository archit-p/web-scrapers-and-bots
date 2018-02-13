from selenium import webdriver
import time
import requests
from lxml import html

# function to get a proxy from gimmeproxy.com
def get_proxy():
    proxy_url = "http://gimmeproxy.com/api/getProxy?protocol=http"

    ps = requests.get(proxy_url)

    ip = ps.content.split(',')[2]
    port = ps.content.split(',')[3]

    ip = ip.replace(':', '')
    ip = ip.replace('"', '')
    ip = ip.replace(' ', '')
    ip = ip.replace('\n', '')
    ip = ip.replace('ip', '')

    port = port.replace(':', '')
    port = port.replace('"', '')
    port = port.replace('\n', '')
    port = port.replace(' ', '')
    port = port.replace('port', '')
    return ip + ':' + port


# setting firefox to use the proxy profile
def set_firefox_profile(ip, port):
    fp = webdriver.FirefoxProfile()
    fp.set_preference('network.proxy_type', 1)
    fp.set_preference('network.proxy.http',ip)
    fp.set_preference('network.proxy.http_port', int(port))
    return fp

# main function
def main():
    address = get_proxy()
    address = address.split(':')
    fp = set_firefox_profile(address[0], address[1])
    driver=webdriver.Firefox()
    
    # asking a user for a url(can be modified later)
    url = raw_input("Enter url: ")
    driver.get(url)

    # returns the HTML from the page
    innerHTML = driver.execute_script("return document.body.innerHTML")
    pageHTML = html.document_fromstring(innerHTML)

    # find the table in the page
    table = pageHTML.cssselect(".technicalSummaryTbl")
    
    tableheader = table[0].cssselect("thead th")
    # writing output to a file called output.csv
    filename = "output.csv"
    csv = open(filename, "w")

    # writing table header contents
    for header in tableheader:
        csv.write(header.text_content() + ",")
    csv.write("\n")
    csv.close()

    tablebody = table[0].cssselect("tbody tr")

    # writing table body contents
    csv = open(filename, "a+")
    for tablerow in tablebody:
        for tablecol in tablerow:
            csv.write(tablecol.text_content() + ",")
        csv.write("\n")
    csv.close()

# call to run the main function
if __name__ == "__main__":
    main()
