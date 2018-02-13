from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def setup_headless():
    options = Options()
    options.add_argument("--headless")
    return options
