from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from random import randint
from random import choice
import string
from selenium.webdriver.common.proxy import *
from lxml import html

def get_proxies():
    print("Getting proxies...")
    time.sleep(2);
    proxies = ['35.196.26.166:3128', '50.233.137.37:80', '208.95.62.80:318','50.233.137.33:80']
    return proxies

def select_proxy(proxies):
    proxy = proxies[randint(0, len(proxies)-1)]
    proxy = proxy.split(":")
    pr = {'ip':'','port':''}
    pr['ip'] = proxy[0]
    pr['port'] = proxy[1]
    return pr

def set_profile(pr):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", pr['ip'])
    profile.set_preference("network.proxy.http_port", int(pr['port']))
    profile.set_preference("network.proxy.ssl", pr['ip'])
    profile.set_preference("network.proxy.ssl_port", int(pr['port']))
    return profile
	
def new_user():
    user = {"fname":"",
            "lname":"",
            "email":"",
            "password":"",
            "month":"",
            "date":"",
            "year":""
            }
    return user

def gen_dob():
    year = str(randint(1990,2005))
    month = randint(1,12)
    if(month < 10):
        month = "0" + str(month)
    else :
        month = str(month)
    date = randint(1,28)
    if(date < 10):
        date = "0" + str(date)
    else:
        date = str(date)
    dob = month + ":" + date + ":" + year 
    return dob

def get_email():
    user = new_user()
    fp = open("config.txt", "r")
    email = fp.read()
    email = email.strip()
    email = email.split(":")
    username = email[0].split("@")
    username[0] = username[0] + '+_' + str(randint(20, 99)) + choice(string.letters)
    username = "@".join(username)
    email[0] = username
    email = ':'.join(email)
    return email

def gen_name():
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
    fname = firstnames[randint(0, len(firstnames)-1)]
    lname = lastnames[randint(0, len(lastnames)-1)]
    name = fname + ":" + lname
    return name

def gen_user():
    user = new_user()
    name= gen_name()
    name = name.split(":")
    dob = gen_dob()
    dob = dob.split(":")
    email = get_email()
    email = email.split(":")
    user['email'] = email[0]
    user['password'] = email[1]
    user['month'] = dob[0]
    user['date'] = dob[1]
    user['year'] = dob[2]
    user['fname'] = name[0]
    user['lname'] = name[1]
    return user

def main():
    proxies = get_proxies();
    baseurl = "https://www.nike.com/in/en_gb/launch/"
    pr = select_proxy(proxies)
    num = input("How many accounts?")
    i = 0
    while(i < num):
        profile = set_profile(pr)
        driver = webdriver.Firefox()
        user = gen_user()
        try:
            search_url = "https://duckduckgo.com/?q=nike+launch"
            driver.get(search_url)
        except:
            i -= 1
            continue
        div = driver.find_element_by_id("r1-0")
        link = div.find_element_by_class_name("result__a")
        link.click()
        try:
            login = driver.find_element_by_class_name("js-log-in")
            login.click()
            time.sleep(2)
            signup_btn = driver.find_element_by_link_text("Join now.")
            signup_btn.click()
            time.sleep(2)
        except:
            i -= 1
            proxies.remove(pr)
            continue

        email_field = driver.find_element_by_name("emailAddress")
        email_field.send_keys(user['email'])

        password_field = driver.find_element_by_name("password")
        password_field.send_keys(user['password'])

        fname_field = driver.find_element_by_name("firstName")
        fname_field.send_keys(user['fname'])

        lname_field = driver.find_element_by_name("lastName")
        lname_field.send_keys(user['lname'])

        date_select = Select(driver.find_element_by_id("nike-unite-date-id-mm"))
        date_select.select_by_value(user['month'])

        date_select = Select(driver.find_element_by_id("nike-unite-date-id-dd"))
        date_select.select_by_value(user['date'])

        date_select = Select(driver.find_element_by_id("nike-unite-date-id-yyyy"))
        date_select.select_by_value(user['year'])

        gender = driver.find_element_by_xpath("/html/body/div[10]/div[2]/div[1]/div/div[1]/div/div[2]/form/div[8]/ul/li[1]/span")
        gender.click()
        gender.click()

if __name__ == "__main__":
    main()
