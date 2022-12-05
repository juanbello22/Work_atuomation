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

def check_exists(option , id):
    try:
        WebDriverWait(driver, 1).until(EC.visibility_of_element_located(((option, id))))
    except TimeoutException:
        return False
    return True

def login(username, password):
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'login_username'))).send_keys(username)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'login_password'))).send_keys(password)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'button_login'))).click()

def open_id_tickets():
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'sidebar_requests'))).click()
    if check_exists(By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"):
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"))).click()
    else: 
        print("Todos los tickets de ID validation fueron cerrados")
        exit()

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
    driver.switch_to.frame(WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@title='Rich Text Editor, reply_textarea']"))))
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//body//p'))).send_keys('-')
    driver.switch_to.default_content()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'submit_button'))).click()
    time.sleep(2)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Select an option']"))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Glober no respondió')]"))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'submit-button'))).click()

#initializing variables
username = input("Invgate user: ")
password = getpass.getpass()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
mails = []

#open invgate 
driver.get("https://globant.cloud.invgate.net/")
login(username, password)
open_id_tickets()

while True:
    time.sleep(1)
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.PAGE_UP)
    charge_and_close()
    time.sleep(1)
    open_id_tickets()