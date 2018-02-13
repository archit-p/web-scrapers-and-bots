from selenium import webdriver
import requests
from lxml import html
import time

browser = webdriver.Firefox()
browser.get("http://www.sslproxies.org")
i = 1
proxies = list()
while(i < 6):
    next_button = browser.find_element_by_link_text("Next")
    HTMLelem = browser.execute_script("return document.body.innerHTML")
    innerHTML = html.fromstring(HTMLelem)
    trs = innerHTML.cssselect("#proxylisttable tbody tr")
    for tr in trs:
        pr = {'ip':'', 'port':''}
        tds = tr.cssselect("td")
        pr['ip'] = tds[0].text_content()
        pr['port'] = tds[1].text_content()
        proxies.append(pr)
    try:
        next_button.click()
        i += 1
    except:
        print("Couldn't click")
        break
browser.close()
nump = int(len(proxies))
print(proxies)

print(nump)

url = "https://dribbble.com/session/new"
logfile = open("logfile", "w")

ac = open("accounts.csv", "r")
accounts = ac.read()
accounts = accounts.split("\n")
i = 0
like_link = raw_input("Enter link to like:")
num_likes = raw_input("How many likes? =  ")
logfile.write(like_link + "\n")
logfile.close()

for i in range(0, int(num_likes)):
    if(accounts[i] == ""):
        continue
    if(i == 0):
        i += 1
        continue
    account = accounts[i].split(",")
    pr = proxies[i%nump]
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
        browser.get(url)
    except:
        print("Coudln't load site")
    try:
        print("Signing in to the account... " + account[0])
        login = browser.find_element_by_id("login")
        login.send_keys(account[2])
        password = browser.find_element_by_id("password")
        password.send_keys(account[3])
        signin = browser.find_element_by_class_name("button")
        signin.click()
        time.sleep(5)
    except:
        print("Couldn't sign in")
    try:
        browser.get(like_link)
        like = browser.find_element_by_class_name("like-shot")
        try:
            curr_like = browser.find_element_by_class_name("current-user-likes")
            print("User already likes")
        except:
            like.click()
    
            logfile = open("logfile", "a+")
            logfile.write(account[0] + "\n")
            logfile.close()
            
            print("Liked post " + str(i-1) + " times")
    except:
        print("Failed to like")
    try:
        signout = browser.find_element_by_link_text("Sign Out")
        signout.click()
    except:
        print("Couldn't sign-out automatically, please do so manually.")
        time.sleep(10)
    i += 1

num_views = input("How many views? = ")
print("Increasing views by " + str(num_views))
for j in range(0, num_views):
    pr = proxies[i%nump]
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
        browser.get(like_link)
        j += 1
        time.sleep(5)
        browser.close()	
    except:
        print("Proxy not configured correctly. Retrying...")		
