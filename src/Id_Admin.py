import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

def check_exists(option , id):
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(((option, id))))
    except TimeoutException:
        return False
    return True

def login():
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'login_username'))).send_keys('j.bello')
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'login_password'))).send_keys('Cod3988b!')
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'button_login'))).click()

def login_admin():
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='identifierId']"))).send_keys('juan.bello@globant.com')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'identifierNext'))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys('Cod2023b!')
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'passwordNext'))).click()
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
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'sidebar_requests'))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"))).click()

def charge_and_close():
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,'@globant.com'))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'request_toolbar_time'))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,'result_time'))).send_keys('5')
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@title='Select a category']"))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Work [Real Time]']"))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'button-silver'))).click()
    if check_exists(By.ID,'popup_option_yes'):
        driver.find_element(By.ID, 'popup_option_yes').click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'request_toolbar_menu'))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='dropDownWindow']//a[@id='time_solve_action']"))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'popup_option_no'))).click()
    driver.switch_to.frame(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@title='Rich Text Editor, reply_textarea']"))))
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//body//p'))).send_keys('-')
    driver.switch_to.default_content()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'submit_button'))).click()
    time.sleep(2)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Select an option']"))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Glober no respondió')]"))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'submit-button'))).click()

#initializing variables
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
mails = []

#open invgate and get mails 
driver.get("https://globant.cloud.invgate.net/")
login()
open_id_tickets()
html = driver.find_element(By.TAG_NAME, 'html')
html.send_keys(Keys.PAGE_DOWN)
time.sleep(1)
html.send_keys(Keys.PAGE_UP)

raw_tickets = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT,'@globant.com')))
for mail in raw_tickets:
    mails.append(get_mail(mail))
print(mails)

driver.execute_script("window.open('about:blank', 'secondtab');")
# It is switching to second tab now
driver.switch_to.window("secondtab")
# In the second tab, it opens google admin
driver.get('https://admin.google.com/')
login_admin()
driver.get("https://admin.google.com/ac/devices/list?status=6&category=all")

for mail in mails:
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).clear()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).send_keys(mail)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).send_keys(Keys.ENTER)
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Select all rows']"))).click()
    except:
        continue
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ow30']"))).click()
    time.sleep(1)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Delete Devices')]"))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Delete')]"))).click()

time.sleep(5)