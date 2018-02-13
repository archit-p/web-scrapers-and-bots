from selenium import webdriver
import time
import requests
from lxml import html

# function to get a proxy from gimmeproxy.com
def get_proxy():
    proxy_url = "http://gimmeproxy.com/api/getProxy?protocol=http"

    ps = requests.get(proxy_url)

    ip = ps.content.split(',')[2]
    port = ps.content.split(',')[3]

    ip = ip.replace(':', '')
    ip = ip.replace('"', '')
    ip = ip.replace(' ', '')
    ip = ip.replace('\n', '')
    ip = ip.replace('ip', '')

    port = port.replace(':', '')
    port = port.replace('"', '')
    port = port.replace('\n', '')
    port = port.replace(' ', '')
    port = port.replace('port', '')
    return ip + ':' + port


# setting firefox to use the proxy profile
def setup_profile(ip, port):
    fp = webdriver.FirefoxProfile()
    fp.set_preference('network.proxy_type', 1)
    fp.set_preference('network.proxy.http',ip)
    fp.set_preference('network.proxy.http_port', int(port))
    return fp
