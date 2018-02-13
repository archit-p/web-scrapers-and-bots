from selenium import webdriver
from lxml import html
from urlparse import urlsplit

def scroll_by(driver, amount):
    i = 0
    while(i < amount):
        driver.execute_script("window.scrollBy(0, 10)")
        i += 1

def scrape_page(driver, filename):
    i = 0
    ceolinks = list()
    innerHTML = driver.execute_script("return document.body.innerHTML")
    page = html.document_fromstring(innerHTML)
    names = page.cssselect(".name")
    titles = page.cssselect(".title")

    filename = filename + ".csv"
    csv = open(filename, "w")
    csv.write("Name, Title\n")
    csv.close()
    print("----------------------------\n\n" + "Working on " + filename + "\n\n\n----------------------------")
    for i in range(0, len(names)):
        csv = open(filename, "a+")
        assert csv is not None
        try:
            csv.write(names[i].text_content().encode('utf8') + "," + titles[i].text_content().encode('utf8').replace(",", "-") + "\n")
        except:
            print("Continue")
        csv.close()

driver = webdriver.Firefox()

driver.get("http://www.earn.com/lists")
driver.maximize_window()
i = 0

scroll_by(driver, 1800)

innerHTML= driver.execute_script("return document.body.innerHTML")
page = html.document_fromstring(innerHTML)
links = page.cssselect(".visible a")

pagelinks = list()
for link in links:
    link = link.get('href')
    link = "http://www.earn.com" + link
    pagelinks.append(link)

for link in pagelinks:
    driver.get(link)
    spliturl = urlsplit(link)
    endurl = spliturl[2]
    filename = endurl[1:-1]
    print(filename)
    scroll_by(driver, 300)
    try:
        button = driver.find_element_by_class_name("pagination-button")
        while(1):
            button.click()
            scroll_by(driver, 300)
            try:
                button = driver.find_element_by_class_name("pagination-button")
            except:
                break;
    except:
        print("No view more")
    scrape_page(driver, filename)
