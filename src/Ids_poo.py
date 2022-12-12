import time
import getpass
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from decouple import config

'''class WebObject:
    '' any interactable object on the webpage (can be a clickable object or one that accepts inputs) ''
    def __init__(self,locator,name):
        self.locator = locator
        self.name = name

    def check_exists(self):
            try:
                WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located(((self.locator, self.name))))
            except TimeoutException:
                return False
            return True

    def clickk(self):
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((self.locator, self.name))).click()

    def send_keyss(self, content):
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((self.locator, self.name))).send_keys(content)

    def get_mails(self):
        raw = str(self.text)
        mail = ''

        if "from " in raw:
            mail = raw.split("from ")[1]
        else:
            mail = raw.split("user ")[1]
        return mail
'''

def check_exists(locator, name):
    try:
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located(((locator, name))))
    except TimeoutException:
        return False
    return True

def get_mail(web_object):
    '''casts web oject to str and then extracts the mail from a bigger piece of string'''
    raw = str(web_object.text)
    mail = ''

    if "from " in raw:
        mail = raw.split("from ")[1]
    else:
        mail = raw.split("user ")[1]
    return mail

class Platform:
    ''' neither Invgate or google admin '''
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

    def open(self):
        DRIVER.get(self.url)

    def switch(self):
        '''opens a new tab with the url of the platform'''
        #Opens a new and blank tab
        DRIVER.execute_script("window.open('about:blank', 'secondtab');")
        # It is switching focus to second tab now
        DRIVER.switch_to.window("secondtab")
        self.open()
        
class Invgate(Platform):
    def login(self):
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'login_username'))).send_keys(self.username)
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'login_password'))).send_keys(self.password)
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'button_login'))).click()

    def close(mail):
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, mail))).click()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'request_toolbar_time'))).click()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID,'result_time'))).send_keys('5')
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@title='Select a category']"))).click()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Work [Real Time]']"))).click()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'button-silver'))).click()
        if check_exists(By.ID,'popup_option_yes'):
            DRIVER.find_element(By.ID, 'popup_option_yes').click()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'request_toolbar_menu'))).click()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='dropDownWindow']//a[@id='time_solve_action']"))).click()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'popup_option_no'))).click()
        DRIVER.switch_to.frame(WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@title='Rich Text Editor, reply_textarea']"))))
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, '//body//p'))).send_keys('-')
        DRIVER.switch_to.default_content()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'submit_button'))).click()
        time.sleep(2)
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Select an option']"))).click()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Glober no respondió')]"))).click()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'submit-button'))).click()

    def open_tkts():
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'sidebar_requests'))).click()
        if check_exists(By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"):
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"))).click()
        else: 
            print("Todos los tickets de ID validation fueron cerrados")  

class Admin(Platform):
    
    def login(self):
            WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='identifierId']"))).send_keys(self.username)
            WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.ID, 'identifierNext'))).click()
            WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(self.password)
            WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.ID, 'passwordNext'))).click()
            time.sleep(8)

    def close():
            for mail in MAILS:
                WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).clear()
                WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).send_keys(mail)
                WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).send_keys(Keys.ENTER)
                try:
                    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Select all rows']"))).click()
                except:
                    continue
                WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ow30']"))).click()
                time.sleep(1)
                WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Delete Devices')]"))).click()
                WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Delete')]"))).click()

    def open(self):
        '''open google admin and then go to "devices" '''
        DRIVER.get('https://admin.google.com/')
        self.login()
        DRIVER.get("https://admin.google.com/ac/devices/list?status=6&category=all")

#initializing variables
INVG_USER, INVG_PASS = config('INVG_USER'), config('INVG_PASS')
ADMIN_USER, ADMIN_PASS = config('ADMIN_USER'), config('ADMIN_PASS')
INVGATE, ADMIN = Invgate(INVG_USER, INVG_PASS, "https://globant.cloud.invgate.net/"), Admin(INVG_USER, INVG_PASS, 'https://admin.google.com/')
DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
HTML = DRIVER.find_element(By.TAG_NAME, 'html') #this variable is used to interact with the html to scroll up and down the page
MAILS = []

#open invgate and get mails 
INVGATE.open()
INVGATE.login()
INVGATE.open_tkts()
HTML.send_keys(Keys.PAGE_DOWN)
time.sleep(1)
HTML.send_keys(Keys.PAGE_UP)

raw_tickets = WebDriverWait(DRIVER, 5).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT,'@globant.com')))
for mail in raw_tickets:
    MAILS.append(get_mail(mail))
print(MAILS)

for mail in MAILS:
    INVGATE.close(mail)
    time.sleep(1)
    INVGATE.open_tkts()

ADMIN.switch()
DRIVER.get("https://admin.google.com/ac/devices/list?status=6&category=all")
ADMIN.close()