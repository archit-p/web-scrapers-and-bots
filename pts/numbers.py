from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
from lxml import html

baseurl = "http://nummer.pts.se"
browser = webdriver.Firefox()
url = "http://e-tjanster.pts.se/telefoni/"
browser.get(url)
filename = "numbers.csv"
previous_operator = 'Telia Sverige AB'

raw_input("Press any key to CONTINUE (after opening the search page)")
print('Searching by operator')

select = Select(browser.find_element_by_id('NumberPlanId'))
select.select_by_value('0')

select = Select(browser.find_element_by_id('OperatorId'))
select.select_by_value('148')

select = Select(browser.find_element_by_id('ServiceTypeId'))
select.select_by_value('10')

submit_btn = browser.find_element_by_id('buttonID')
submit_btn.click()

time.sleep(2)

visas = browser.find_elements_by_link_text("Visa")
hrefs = list()
for visa in visas:
    hrefs.append(visa.get_attribute('href'))
    
for href in hrefs:
    browser.get(href)
    innerHTML = browser.execute_script("return document.body.innerHTML")
    htmlElem = html.document_fromstring(innerHTML)
    tds = htmlElem.cssselect("tbody td")
    print('Found ' + str(len(tds)/3) + ' phone numbers')
    i = 0
    for td in tds:
        fd = open(filename, 'a+')
        if(i%3 == 0):
            number = td.text_content()
            print('Writing ' + number + 'to file')
            fd.write(number + ',')
        elif(i%3 == 1):
            operator = td.text_content()
            fd.write(operator.encode('utf8' + ','))
            fd.write(previous_operator + ',')
        else:
            date = td.text_content()
            fd.write(date + '\n')
        fd.close()
        i += 1    
