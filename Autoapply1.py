from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from colorama import init, Fore, Style
from time import sleep, time
from random import randint, choice, uniform
import json
import os 
from pwinput import pwinput

##Terminal Color
init(convert=True)
init(autoreset=True)

bright=Style.BRIGHT
dim=Style.DIM
red=Fore.RED+dim
green=Fore.GREEN+dim
cyan=Fore.CYAN+bright
yellow=Fore.LIGHTYELLOW_EX+dim
blue = Fore.BLUE + dim
white = Fore.WHITE + dim
magenta = Fore.MAGENTA + dim

# Config
URL_ROOT = "https://www.linkedin.com/"
CONFIG_FILE = "Config.json"
LOGIN_MAX_RETRIES = 10

def cleanCS():
    os.system('cls' if os.name=='nt' else 'clear')

class AutoApplier:
    def _init_(self,
               username,
               password,
               loc_list,
               experience,
               keywords,
               is_silent):
        self.username=username #account infor-email|phone number
        self.password=password
        self.loc_list=loc_list
        self.experience=experience
        self.keywords=keywords
        self.is_silent=is_silent

    def create_session(self):
        options = Options()

        # Standard settings
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--log-level=3")

        # Run chrome on the background
        if self.is_silent:
            options.headless = True
            mode_str = "Headless"
        else:
            mode_str = "Visible"

        # Avoid detection 1
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Create session
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # Avoid detection 2
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": "Mozilla/5.0 (X11; CrOS x86_64 13904.97.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.167 Safari/537.36"})
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("\n{}[Created selenium session - {} mode]\n\n".format(green, mode_str))

        return self.driver

    def fill_infor(self, object, text):
        sleep(uniform(0.1,0.3))#fill in random time 0.1-0.3s 
        object.click()
        for char in text:
            object.send_keys(char)
            sleep(uniform(0.04,0.13))
        sleep(uniform(0.1,0.3))
        
    def do_login(self):
        driver=self.driver #create driver

        #in case driver goes to main page without direct login 
        page=driver.get(URL_ROOT)
        go_Login=driver.find_element_by_class_name("nav__button-secondary").click()

        User_info = driver.find_element_by_name("session_key") #account infor-email|phone number
        self.fill_infor(User_info,self.username)

        Password=driver.find_element_by_name("session_password")
        self.fill_infor(Password,self.password)

        Login=driver.find_element_by_class_name("login__form_action_container ").click()


        #handle Captcha challenge
        while True:
            try:
                checkpoint_element=driver.find_element_by_id("captchaInternalPath")
            except:
                break
            print("{}CHALLENGE REQUIRED".format(yellow))
            sleep(3)
        
        #handle email verification
        while True:
            try:
                email_verify = driver.find_element_by_id("input__email_verification_pin")
            except:
                break
            print("{}EMAIL VERIFICATION REQUIRED".format(yellow))
            sleep(3)

        
        count = 0
        while True:
            try:
                message_list = driver.find_element_by_id("msg-overlay")
                break
            except Exception as error:
                if count >= LOGIN_MAX_RETRIES:
                    return False
                print("{}Waiting for feed to load ({}/{})".format(yellow))
                sleep(3)
                count += 1

        return True

    def get_location(self):
        driver = self.driver
        loc_list = self.loc_list
        
        driver.get(URL_ROOT + "jobs/")
        sleep(3)
        job_location_field = driver.find_elements_by_class_name("jobs-search-box__inner")[1]
        last_loc = driver.current_url
        added_count = 0
        
        for loc in loc_list:
            if loc_list[loc] == "":
                job_location_field.click()
                sleep(3.5)
                actions = ActionChains(driver)
                actions.send_keys(loc)
                actions.perform()
                print("Click on the location you wish to use for \'{}\' and press enter".format(loc))
                while True:
                    input()
                    if last_loc == driver.current_url:
                        print(red + "You must select a location first")
                        continue
                    else:
                        # pretty messy
                        try:
                            loc_list[loc] = driver.current_url
                            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                data["locations"][loc] = driver.current_url
                                f.close()
                                
                            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False)
                                f.close()
                            
                            print("{}Added {}".format(green, loc))
                            added_count += 1
                            break
                        except Exception as error:
                            print("{}Error adding {}".format(red, loc))
                            print(error)
                            
            else:
                added_count += 1
                
        if added_count == 0:
            raise ValueError('Geographical location setup failed')
        else:
            print("{}Geographical location setup finished".format(yellow))
            return loc_list
            





