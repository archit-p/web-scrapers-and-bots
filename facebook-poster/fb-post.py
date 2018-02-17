from selenium import webdriver
import random
import time
import geturl
import proxy
from selenium.webdriver.firefox.options import Options

URL = 'http://facebook.com'
email = ''
password = ''
groupURL = raw_input('Please enter the groupURL: ')

def login(browser):
    browser.get(URL)
    emailele = browser.find_element_by_id('email')
    emailele.send_keys(email)
    passwordele = browser.find_element_by_id('pass')
    passwordele.send_keys(password)
    button = browser.find_element_by_id('loginbutton')
    button.click()

def get_message():
    fp = open('messages.csv', 'r')
    content = fp.read()
    messages = content.split('\n')
    print(messages)
    while(msg == ''):
        i = random.randint(1, len(messages)-1)
        msg = messages[i]
    return msg

def prep_message(msg, link, name, hashtag):
    msg = msg.replace('{link}', link)
    msg = msg.replace('{name}', name)
    msg = msg.replace('{hashtag}', hashtag)
    return msg

def random_link():
    fp = open('youtube-links.csv', 'r')
    content = fp.read()
    fp.close()
    links = content.split('\n')
    link = ''
    while(link == ''):
        i = random.randint(1, len(links))
        link = links[i]
    links.remove(link)
    content = '\n'.join(links)
    fp = open('youtube-links.csv', 'w')
    fp.write(content)
    return link

def setup_headless():
    options = Options()
    options.add_argument("--headless")
    return options

def main():
    geturl.main()
    time.sleep(5)
    link = random_link()
    name = raw_input('Enter name: ')
    hashtag = raw_input('Enter hashtag: ')
    proxy_choice = raw_input('Do you want to use proxies? (yes/no)')
    print('Logggin in using\nUsername=' + email + '\nPassword=' + password)
    if(proxy_choice == 'yes'):
        proxies = proxy.get_proxy()
        i = random.randint(0, len(proxies)-1)
        pr = proxies[i]
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", pr['ip'])
        profile.set_preference("network.proxy.http_port", int(pr['port']))
        profile.set_preference("network.proxy.ssl", pr['ip'])
        profile.set_preference("network.proxy.ssl_port", int(pr['port']))
        options = setup_headless()
        browser = webdriver.Firefox(firefox_options=options)
        login(browser)
    else:
        options = setup_headless()
        browser = webdriver.Firefox(firefox_options=options)
        login(browser)

    while True:
        print('Visitng group URL')
        browser.get(groupURL)
        tb = browser.find_element_by_name('xhpc_message_text')
        message = get_message()
        msg = prep_message(message, link, name, hashtag)
        print('Posting')
        time.sleep(5)
        print(msg)
        tb.send_keys(msg)
        time.sleep(5)
        try:
            post_btn = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div/div[2]/button')
            post_btn.click()
            break
        except Exception as e:
            print(e)
    browser.close()

if __name__ == '__main__':
    main()
