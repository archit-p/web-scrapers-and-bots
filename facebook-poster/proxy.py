from selenium import webdriver
from lxml import html

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
print(proxies)
