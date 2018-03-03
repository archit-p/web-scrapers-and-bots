from selenium import webdriver
import random
import time
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys

class NapsterBot():
    def __init__(self, proxy_lock, login_lock, wait_time, play_time, playlist_url):
        self.proxy_lock = proxy_lock;
        self.login_lock = login_lock;
        self.proxy = self.get_proxy()
        self.driver = webdriver.Firefox(firefox_profile=self.setup_profile(self.proxy['ip'], self.proxy['port']));
        self.wait_time = wait_time;
        self.play_time = play_time;
        self.playlist_url = playlist_url;

    def setup_profile(self, ip, port):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", ip)
        profile.set_preference("network.proxy.http_port", int(port))
        profile.set_preference("network.proxy.ssl", ip)
        profile.set_preference("network.proxy.ssl_port", int(port))
        return profile

    def get_credentials(self):
        self.login_lock.acquire()
        print("Opening account file")
        details = ''
        with open('accounts.csv', 'r+') as login_file:
            details = login_file.read();
            details = details.split('\n');
            user = {'username':'', 'password':''};
            detail = details[0].split(",")
            print(detail)
            user['username'] = detail[0];
            user['password'] = detail[1];
            detail = ','.join(detail);
            print(user)
        #with open('accounts.csv', 'w') as login_file:
        #    details.remove(detail);
        #    details = '\n'.join(details)
        #    login_file.write(details)
        print("Closing account file")
        self.login_lock.release()
        return user;

    def get_proxy(self):
        self.proxy_lock.acquire()
        print("Opening proxy file")
        proxy = {'ip':'','port':''}
        with open('proxies.csv', 'r+') as proxy_file:
            details = proxy_file.read();
            details = details.split('\n');
            print(details)

            # select a random proxy from the file
            num = random.randint(0, len(details)-1);
            detail = details[num].split(":");
            while(detail[0] == ''):
                num = random.randint(0, len(details)-1);
                detail = details[num].split(":");
            print(detail);
            proxy['ip'] = detail[0];
            proxy['port'] = detail[1];
            print(proxy)
        print("Closing proxy file")
        self.proxy_lock.release()
        return proxy

    def handle_playlist(self):
        self.driver.get(self.playlist_url);
        play_btns = self.driver.find_elements_by_class_name("play-button");
        for play_btn in play_btns:
            hoverover = ActionChains(self.driver).move_to_element(play_btn).click().perform()
            play_btn = self.driver.find_element_by_class_name("play-button");
            play_btn.click();
            time.sleep(5);1
    
    def login(self):
        login_url = "https://us.napster.com/";
        user = self.get_credentials();
        self.driver.get(login_url);
        flag = 0
        while(flag == 0):
            while(1):
                try:
                    time.sleep(5);
                    login_btn = self.driver.find_element_by_link_text("Login");
                    login_btn.click();
                    break;
                except:
                    continue;

            while(1):
                try:
                    id_field = self.driver.find_element_by_id("username");
                    id_field.send_keys(user['username']);
                    time.sleep(2);
                    pwd_field = self.driver.find_element_by_id("password");
                    pwd_field.send_keys(user['password']);
                    time.sleep(2);
                    signin_btn = self.driver.find_element_by_class_name("signin");
                    signin_btn.click();
                    time.sleep(15);
                    break;
                except:
                    continue;

            try:
                login_btn = self.driver.find_element_by_link_text("Login");
            except:
                flag = 1;

    def main(self):
        #self.login();
        self.handle_playlist();
        time.sleep(20);
        #self.driver.close();
