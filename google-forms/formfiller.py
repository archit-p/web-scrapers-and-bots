from selenium import webdriver
import requests
from lxml import html
import random
from selenium.webdriver.support.ui import Select
import time
import re

def get_details():
    # url to get fake address
    addr_url = "https://fakena.me/fake-name/"
    url = "https://fakena.me/random-real-address/"
    # file for emails
    email_file = "emails.csv"

    # open file and get emails
    emailfd = open(email_file,"r")
    emails = emailfd.read()
    emailfd.close()
    emails = emails.split("\n")

    addr_response = requests.get(addr_url)
    time.sleep(5)
    addr_html = html.document_fromstring(addr_response.content)


    response = requests.get(url)
    time.sleep(5)
    responsehtml = html.document_fromstring(response.content)

    address = responsehtml.cssselect("strong")[0].text_content()
    address = address.split(' ')

    print(address)

    city_init = address[-3]
    state = address[-2]
    zipcode = address[-1]
    zipcode_split = zipcode.split('-')

    city = re.findall('[A-Z][^A-Z]*', city_init)
    if(len(city_init) > 1):
        address.append(city[0])
        city = city[-1]


    address.remove(city_init)
    address.remove(state)
    address.remove(zipcode)

    trs = addr_html.cssselect("tr")

    # find trs with the information
    for tr in trs:
        if "Name:" in tr.text_content():
            name_tr = tr
        if "Phone" in tr.text_content():
            phone_tr = tr

    # dictionary to hold details
    details = {'fname':'',
            'lname':'',
            'street':'',
            'city':'',
            'state':'',
            'zip':'',
            'phone':'',
            'email':'',
            'tickets':''
            }

    # update the details into the dictionary
    details['fname'] = name_tr.cssselect("td")[1].text_content().split(' ')[0]
    details['lname'] = name_tr.cssselect("td")[1].text_content().split(' ')[1]
    details['city'] = city.replace(',', '')
    details['state'] = state
    details['zip'] = zipcode_split[0]
    details['street'] = ' '.join(address).replace(',', '')
    details['phone'] = phone_tr.cssselect("td")[1].text_content().replace("(", "").replace(")", "").replace(" ", "-")
    details['email'] = emails[0]
    details['tickets'] = random.randint(1,4)


    # exit if the file doesn't contain enough emails
    if(details['email'] == ''):
        print("The file doesn't contain enough emails")
        exit()

    # delete the email and resubmit the file
    emails.remove(emails[0])
    emails = '\n'.join(emails)
    emailfd = open(email_file, "w")
    emailfd.write(emails)
    emailfd.close()

    return details

def write_to_file(details):
    logfile = "log.csv"

    logfd = open(logfile, "a+")
    logfd.write(details['fname'] + "," + details['lname'] + "," + details['street'] + "," + details['city'] + ',' + details['state'] + "," + details['zip'] + "," + details['phone'] + "," + details['email'] + "," + str(details['tickets']) + "\n")
    logfd.close()

def form_filler():
    # get details
    print("-------------------------------------------------------------\n\nGenerating new details...\n\n")
    details = get_details()
    print(details)

    # url for the form
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdYfn_8HnKgB2sRjT2up1-S_kxMONHCQS0VXq_XdEv7S-Hd4w/viewform?embedded=true"

    # open a new browser window
    browser = webdriver.Firefox()
    time.sleep(4)
    browser.get(form_url)
    try:
        # find the input fields in the form
        fname_field = browser.find_element_by_id("entry_542750204")
        lname_field = browser.find_element_by_id("entry_783589459")
        address_field = browser.find_element_by_id("entry_955731740")
        city_field = browser.find_element_by_id("entry_1706274227")
        zip_field = browser.find_element_by_id("entry_1745636381")
        phone_field = browser.find_element_by_id("entry_1037997524")
        email_field = browser.find_element_by_id("entry_838774160")
        ticket_field = Select(browser.find_element_by_id("entry_161676395"))
        state_field = Select(browser.find_element_by_id("entry_1933491622"))
        submit_btn = browser.find_element_by_id("ss-submit")

        # fill the form
        fname_field.send_keys(details['fname'])
        lname_field.send_keys(details['lname'])
        address_field.send_keys(details['street'])
        city_field.send_keys(details['city'])
        zip_field.send_keys(details['zip'])
        phone_field.send_keys(details['phone'])
        email_field.send_keys(details['email'])
        ticket_field.select_by_value(str(details['tickets']))
        state_field.select_by_value(details['state'])
        submit_btn.click()
        print("\n\n-------------------------------------------------------------\n")
        time.sleep(2)
        browser.close()

    except:
        print("ERROR! Page couldn't load correctly.Retrying!")
    write_to_file(details)

def main():
    num = input("How many times do you want to fill the form? = ")
    waittime = input("How many seconds do you want to wait? = ")
    for i in range(0, num):
        form_filler()
        print("Filled form " + str(i + 1) + " times!")
        time.sleep(waittime)

if __name__ == "__main__":
    main()
