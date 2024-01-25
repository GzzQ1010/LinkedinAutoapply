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
        self.username=username
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

        