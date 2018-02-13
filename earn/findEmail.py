from lxml import html
from selenium import webdriver

def email_finder(name):
    driver = webdriver.Firefox()
    baseurl = "http://www.google.com/search?q="
    company_name = raw_input("Company name: ")
    searchurl = baseurl + company_name
    response = driver.get(searchurl)
    searchhtml = driver.execute_script("return document.body.innerHTML")
    pagehtml = html.document_fromstring(searchhtml)
    links = pagehtml.cssselect(".r a")
    domain_orig = links[0].get('href')
    if "www" in domain_orig:
        domain = domain_orig[12:-1]
    else:
        domain = domain_orig[8:-1]
    email = name.split()[0] + "@" + domain
    print(email)
