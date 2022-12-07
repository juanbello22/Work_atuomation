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

def check_exists(option , id):
    try:
        WebDriverWait(Driver, 1).until(EC.visibility_of_element_located(((option, id))))
    except TimeoutException:
        return False
    return True

def login(username, password):
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.ID, 'login_username'))).send_keys(username)
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.ID, 'login_password'))).send_keys(password)
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.ID, 'button_login'))).click()

def login_admin(username, password):
    WebDriverWait(Driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='identifierId']"))).send_keys(username)
    WebDriverWait(Driver, 10).until(EC.visibility_of_element_located((By.ID, 'identifierNext'))).click()
    WebDriverWait(Driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(password)
    WebDriverWait(Driver, 10).until(EC.visibility_of_element_located((By.ID, 'passwordNext'))).click()
    time.sleep(8)

def get_mail(web_object):
    raw = str(web_object.text)
    mail = ''

    if "from " in raw:
        mail = raw.split("from ")[1]
    else:
        mail = raw.split("user ")[1]
    return mail

def open_id_tickets():
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.ID, 'sidebar_requests'))).click()
    if check_exists(By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"):
        WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"))).click()
    else: 
        print("Todos los tickets de ID validation fueron cerrados")

def charge_and_close(mail):
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, mail))).click()
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.ID, 'request_toolbar_time'))).click()
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.ID,'result_time'))).send_keys('5')
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@title='Select a category']"))).click()
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Work [Real Time]']"))).click()
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'button-silver'))).click()
    if check_exists(By.ID,'popup_option_yes'):
        Driver.find_element(By.ID, 'popup_option_yes').click()
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.ID, 'request_toolbar_menu'))).click()
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='dropDownWindow']//a[@id='time_solve_action']"))).click()
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.ID, 'popup_option_no'))).click()
    Driver.switch_to.frame(WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@title='Rich Text Editor, reply_textarea']"))))
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//body//p'))).send_keys('-')
    Driver.switch_to.default_content()
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.ID, 'submit_button'))).click()
    time.sleep(2)
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Select an option']"))).click()
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Glober no respondió')]"))).click()
    WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.ID, 'submit-button'))).click()

def close_admin():
    for mail in Mails:
        WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).clear()
        WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).send_keys(mail)
        WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).send_keys(Keys.ENTER)
        try:
            WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Select all rows']"))).click()
        except:
            continue
        WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ow30']"))).click()
        time.sleep(1)
        WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Delete Devices')]"))).click()
        WebDriverWait(Driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Delete')]"))).click()

#initializing variables
Invg_user = config('INVG_USER')
Invg_pass = config('INVG_PASS')
Admin_user = config('ADMIN_USER')
Admin_pass = config('ADMIN_PASS')
Driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
Mails = []

#open invgate and get mails 
Driver.get("https://globant.cloud.invgate.net/")
login(Invg_user, Invg_pass)
open_id_tickets()
html = Driver.find_element(By.TAG_NAME, 'html')
html.send_keys(Keys.PAGE_DOWN)
time.sleep(1)
html.send_keys(Keys.PAGE_UP)
raw_tickets = WebDriverWait(Driver, 5).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT,'@globant.com')))

for mail in raw_tickets:
    Mails.append(get_mail(mail))
print(Mails)

for mail in Mails:
    charge_and_close(mail)
    time.sleep(1)
    open_id_tickets()

Driver.execute_script("window.open('about:blank', 'secondtab');")
# It is switching to second tab now
Driver.switch_to.window("secondtab")
# In the second tab, it opens google admin
Driver.get('https://admin.google.com/')
login_admin(Admin_user, Admin_pass)
Driver.get("https://admin.google.com/ac/devices/list?status=6&category=all")
close_admin()
