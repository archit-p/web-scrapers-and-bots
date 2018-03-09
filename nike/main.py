from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from random import randint
from random import choice
import string
from selenium.webdriver.common.proxy import *
from lxml import html

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
    year = str(randint(1980,1996))
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
    print("New user details generated are \n" + str(user))
    return user

def write_to_log(fname, lname, email, password):
    print("Writing " + email + ":" + password + "to file.")
    fp = open("log.csv", "a+")
    fp.write(fname + "," + lname + "," + email + "," + password + "\n");
    fp.close()
    return

def main():
    pr = {'ip':'34.206.205.194','port':'41700'}
    num = input("How many accounts? ")
    profile = set_profile(pr)
    driver = webdriver.Firefox(firefox_profile=profile)
    i = 0
    while(1):
        user = gen_user()
        try:
            search_url = "https://duckduckgo.com/?q=nike+launch"
            driver.get(search_url)
        except:
            print("Looks like the page is acting weird. RELOADIN'!")
            num += 1;
            continue
        try:
            div = driver.find_element_by_id("r1-0")
            link = div.find_element_by_class_name("result__a")
            link.click()
            time.sleep(2);
        except:
            print("Looks like the page is acting weird. RELOADIN'!")
            num += 1
            continue
        try:
            login = driver.find_element_by_xpath("/html/body/div[3]/div/header/div/div/nav/div[2]/a[1]")
            login.click()
            time.sleep(2)
            signup_btn = driver.find_element_by_link_text("Join now.")
            signup_btn.click()
            time.sleep(2)
        except:
            print("Looks like the page is acting weird. RELOADIN'!")
            num += 1
            continue

        email_field = driver.find_element_by_name("emailAddress")
        email_field.send_keys(user['email'])

        time.sleep(2);
        password_field = driver.find_element_by_name("password")
        password_field.send_keys(user['password'])

        fname_field = driver.find_element_by_name("firstName")
        fname_field.send_keys(user['fname'])

        lname_field = driver.find_element_by_name("lastName")
        lname_field.send_keys(user['lname'])

        month_select = Select(driver.find_element_by_id("nike-unite-date-id-mm"))
        month_select.select_by_value(user['month'])

        time.sleep(3);
        date_select = Select(driver.find_element_by_id("nike-unite-date-id-dd"))
        date_select.select_by_value(user['date'])

        time.sleep(2);
        year_select = Select(driver.find_element_by_id("nike-unite-date-id-yyyy"))
        year_select.select_by_value(user['year'])

        time.sleep(2);
        spans = driver.find_elements_by_tag_name("span")
        rand = randint(0,1000)
        for span in spans:
            if(rand%2 == 0):
                if "Male" in span.text:
                    gender = span
                else:
                    continue
            else:
                if "Female" in span.text:
                    gender = span
                else:
                    continue

        gender.click()
        gender.click()

        submit = driver.find_element_by_class_name("joinSubmit")
        submit_btn = submit.find_element_by_tag_name("input")
        submit_btn.click()
        submit_btn.click()
        
        while(1):
            try:
                update_select = driver.find_element_by_id("nike-unite-date-id-yyyy")
                try:
                    time.sleep(2);
                    rand = randint(1000, 100000);
                    if(rand%2 == 1):
                        month_select.select_by_value(str(int(user['month']) + randint(-3,0)))
                    else:
                        date_select.select_by_value(str(int(user['date']) + randint(-4,2)))
                    update_select.click()
                    gender.click()
                    submit_btn.click()
                    submit_btn.click()
                except:
                    continue
            except:
                print("Done "+ str(i+1) + " accounts!")
                break
        i += 1
        if(i == num):
            break;
        write_to_log(user['fname'], user['lname'], user['email'], user['password'])
        time.sleep(15);

if __name__ == "__main__":
    main()
