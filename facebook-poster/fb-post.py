from selenium import webdriver

URL = 'http://facebook.com'
email = 'pandey.archit7@gmail.com'
password = 'facebook16189742!'
groupid = '151014724941578'
groupURL = 'http://facebook.com/groups/{}/'.format(groupid)

browser = webdriver.Firefox()
browser.get(URL)
emailele = browser.find_element_by_id('email')
emailele.send_keys(email)
passwordele = browser.find_element_by_id('pass')
passwordele.send_keys(password)
button = browser.find_element_by_id('loginbutton')
button.click()

browser.get(groupURL)
tb = browser.find_element_by_name('xhpc_message_text')
tb.send_keys('Hey guys its been a long time')

browser.close()
