from selenium import webdriver
from lxml import html
import random
import time
from selenium.webdriver.common.proxy import *

MAX_ACCOUNT = 36

firstnames = [
    "Alfred",
    "Andrew",
    "Martin",
    "Harry",
    "Tom",
    "Michael",
    "Peter",
    "Robert",
    "Frank",
    "Matthew",
    "Donald",
    "Phillip",
    "Paul",
    "Dale",
    "Christian",
    "Maria",
    "Stephanie",
    "Evelyn",
    "Caitlyn",
    "Sonny",
    "Julia"
]

initials = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T"
]

lastnames = [
    "Carnegie",
    "Roberts",
    "Clinton",
    "Joyce",
    "Holder",
    "Smith",
    "Owens",
    "Louden",
    "Steffey",
    "Rouse",
    "Stagner",
    "Chausse",
    "White",
    "Brewster",
    "Kelly",
    "Gurley",
    "Morales",
    "Grimes"
]
# get proxies

browser = webdriver.Firefox()
response = browser.get("http://www.sslproxies.org")
HTMLelem = browser.execute_script("return document.body.innerHTML")
innerHTML = html.document_fromstring(HTMLelem)
trs = innerHTML.cssselect("#proxylisttable tbody tr")
proxies = list()
for tr in trs:
    pr = {'ip':'', 'port':''}
    tds = tr.cssselect("td")
    pr['ip'] = tds[0].text_content()
    pr['port'] = tds[1].text_content()
    proxies.append(pr)
browser.close()
baseurl = "http://dribbble.com/signup/new"
filename = "accounts.csv"
fd = open(filename, "r")
filecontent = fd.read()
fd.close()
# dictionary to store account details
details = {'name' : '', 'username' : '', 'email' : '', 'password' : ''}
# emailurl = "http://www.fakemailgenerator.com/#/superrito.com/"

for i in range(0, MAX_ACCOUNT):
    firstname = firstnames[random.randint(0, len(firstnames)-1)]
    lastname = lastnames[random.randint(0, len(lastnames)-1)]
    details['name'] = firstname + ' ' + lastname
    details['email'] = firstname.lower() + lastname.lower() + "@superrito.com"
    details['username'] = firstname.lower() + lastname.lower()
    details['password'] = firstname.lower() + str(random.randint(1111, 2346))
    print(details)
    if(details['name'] in filecontent):
        continue
    pr = proxies[i%len(proxies)]
    myProxy = pr['ip'] + ":" + pr['port']
    print(myProxy)

    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", pr['ip'])
    profile.set_preference("network.proxy.http_port", int(pr['port']))
    profile.set_preference("network.proxy.ssl", pr['ip'])
    profile.set_preference("network.proxy.ssl_port", int(pr['port']))
    browser = webdriver.Firefox(firefox_profile=profile)
    try:
        browser.get(baseurl)
    except:
        browser.close()
        print("Retryin...")
        continue
    try:
        name_field = browser.find_element_by_id("user_name")
        username_field = browser.find_element_by_id("user_login")
        email_field = browser.find_element_by_id("user_email")
        password_field = browser.find_element_by_id("user_password")
        tos_btn = browser.find_element_by_id("user_agree_to_terms")
        submit_btn = browser.find_element_by_class_name("form-sub")

        name_field.send_keys(details['name'])
        username_field.send_keys(details['username'])
        email_field.send_keys(details['email'])
        password_field.send_keys(details['password'])
        tos_btn.click()
        submit_btn.click()
        time.sleep(30)
    
        save = browser.find_element_by_class_name("form-sub")
        save.click()
        time.sleep(5)
        browser.close()

        fd = open(filename, "a+")
        fd.write(details['name'] + "," + details['email'] + "," + details['username'] + "," + details['password'] + "\n")
        fd.close()
    except:
        print("Couldn't load page correctly")
