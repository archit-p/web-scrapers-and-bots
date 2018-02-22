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
    # file for emails
    email_file = "emails.csv"

    # open file and get emails
    emailfd = open(email_file,"r")
    emails = emailfd.read()
    if(emails == ''):
        print("File doesn't contain enough emails. EXITING!")
        exit()
    emailfd.close()
    emails = emails.split("\n")

    mail = emails[0]

    mail = mail.split(",")
    response = requests.get(addr_url)
    addr_html = html.document_fromstring(response.content)

    trs = addr_html.cssselect("tr")

    # find trs with the information
    for tr in trs:
        if "Name:" in tr.text_content():
            name_tr = tr
        if "Phone" in tr.text_content():
            phone_tr = tr
        if "ZIP" in tr.text_content():
            zip_tr = tr

    # dictionary to hold details
    details = {'fname':'',
            'lname':'',
            'zip':'',
            'email':'',
            'password':''
            }

    # update the details into the dictionary
    details['fname'] = name_tr.cssselect("td")[1].text_content().split(' ')[0]
    details['lname'] = name_tr.cssselect("td")[1].text_content().split(' ')[1]
    details['email'] = mail[0]
    details['password'] = mail[1]
    details['zip'] = zip_tr.cssselect("td")[1].text_content().split(' ')[-1]

    # delete the email and resubmit the file
    mail = ','.join(mail)
    emails.remove(mail)
    emails = '\n'.join(emails)
    emailfd = open(email_file, "w")
    emailfd.write(emails)
    emailfd.close()

    return details

def write_to_file(details):
    logfile = "log.csv"

    logfd = open(logfile, "a+")
    logfd.write(details['fname'] + "," + details['lname'] + "," + details['zip'] + "," + details['email'] + "," + details['password'] + "\n")
    logfd.close()

def form_filler():
    # get details
    print("-------------------------------------------------------------\n\nGenerating new details...\n\n")
    details = get_details()
    print("Filling form with following details...")
    print(details)

    form_url = "http://bit.ly/2sEhIR8"
    driver = webdriver.Firefox()
    driver.get(form_url)

    fname_field = driver.find_element_by_id("first_name")
    fname_field.send_keys(details['fname'])

    lname_field = driver.find_element_by_id("last_name")
    lname_field.send_keys(details['lname'])

    email_field = driver.find_element_by_id("email_address")
    email_field.send_keys(details['email'])

    email_field_2 = driver.find_element_by_id("email_address_retype")
    email_field_2.send_keys(details['email'])

    pwd_field = driver.find_element_by_id("password")
    pwd_field.send_keys(details['password'])

    pwd_field_2 = driver.find_element_by_id("password_confirm")
    pwd_field_2.send_keys(details['password'])

    country = Select(driver.find_element_by_id("country_id"))
    country.select_by_value("222")

    zip_field = driver.find_element_by_id("postal_code")
    zip_field.send_keys(details['zip'])

    sbmt_button = driver.find_element_by_id("continue")
    sbmt_button.click()
    driver.close()

    write_to_file(details)
    print("\n\n-------------------------------------------------------------\n\n")

def main():
    num = input("How many times do you want to fill the form? = ")
    waittime = input("How many seconds do you want to wait? = ")
    for i in range(0, num):
        form_filler()
        print("Filled form " + str(i + 1) + " times!")
        time.sleep(waittime)

if __name__ == "__main__":
    main()
