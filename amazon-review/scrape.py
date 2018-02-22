from selenium import webdriver
import re
import time
from Queue import Queue

class scraper:
    def __init__(self):
        self.driver = webdriver.Firefox()
        # enter your amazon email below
        self.email = 'pandey.archit7@gmail.com'
        # enter your amazon password below
        self.password = 'amazon16189742!'
        self.profile_queue = Queue()
        #default output filename is output.csv
        self.filename = "output3.csv"
        fp = open(self.filename, "w")
        fp.write("Rank,Name,Email,Profile Link\n")
        fp.close()

    def write_line_to_file(self, line):
        fp = open(self.filename, "a+")
        fp.write(line + "\n")
        fp.close()

    def write_details_to_file(self, rank, name, email, prof_link):
        line = str(rank) + "," + str(name) + "," + str(email) + "," + str(prof_link)
        self.write_line_to_file(line)

    # login into amazon to view the emails
    def login(self):
        login_url = 'https://www.amazon.de/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=deflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.de%2Fref%3Dnav_signin&switch_account='
        self.driver.get(login_url)
        try:
            email_input = self.driver.find_element_by_id("ap_email")
            email_input.send_keys(self.email)
        except:
            print("Could not find email element. Did you update your email in the file?")
            exit()
        continue_btn = self.driver.find_element_by_id("continue")
        continue_btn.click()
        try:
            pwd_input = self.driver.find_element_by_id("ap_password")
            pwd_input.send_keys(self.password)
        except:
            print("Did you update your account password correctly inside the file?")
            exit()
        signin_btn = self.driver.find_element_by_id("signInSubmit")
        signin_btn.click()
        #raw_input("After veryfying your accout via email or phone please click ANY key to CONTINUE!")
    # generate URLs
    def url_gen(self, page_no):
        base_url = 'https://www.amazon.de/hz/leaderboard/top-reviewers/ref=cm_cr_tr_link_1000?page={}'
        page_url = base_url.format(str(page_no))
        return page_url
    # visit pages one by one
    def handle_list_page(self, page_num):
        url = self.url_gen(page_num)
        while(1):
            try:
                self.driver.get(url)
                break
            except:
                print("Retrying")
        links = self.driver.find_elements_by_class_name("a-link-normal")
        prof_urls = list()
        for link in links:
            prof_url = link.get_attribute("href")
            if "name" in prof_url:
                self.profile_queue.put(prof_url)
        self.handle_profile_pages()

    # find profile links in each page
    def handle_list_pages(self):
        i = 25
        while i <= 1000:
            self.handle_list_page(i)
            time.sleep(8)
            i += 1

    # visit one profile page and get details from there
    def handle_profile_page(self, profile_url):
        while(1):
            try:
                self.driver.get(profile_url)
                break
            except:
                print("Retrying")
        innerHTML = self.driver.execute_script("return document.body.innerHTML")
        p = re.compile('"publicEmail":"[a-zA-Z0-9_.]*@[a-zA-Z]+.[a-zA-Z]+"')
        emails = p.findall(innerHTML)
        if emails == [] or emails == '':
            email = 'null'
        else:
            email = emails[0]
            email = email.replace('publicEmail', '')
            email = email.replace('"', '')
            email = email.strip()
            email = email.replace(':', '')
            email = email.encode('utf8')

        name = self.driver.find_element_by_class_name("a-size-extra-large").text
        profile_url = profile_url.encode('utf8')
        name = name.strip()
        name = name.encode('utf8')

        try:
            more_btn = self.driver.find_element_by_link_text("See More")
            more_btn.click()
        except:
            more_btn = None;

        rank = self.driver.find_element_by_class_name("a-link-normal").text
        rank = rank.replace('Reviewer ranking', '')
        rank = rank.strip()
        rank = rank.encode('utf8')
        self.write_details_to_file(rank, name, email, profile_url)
    # get details from profile pages
    def handle_profile_pages(self):
        while not self.profile_queue.empty():
            profile_link = self.profile_queue.get()
            self.handle_profile_page(profile_link)

s = scraper()
s.login()
s.handle_list_pages()
