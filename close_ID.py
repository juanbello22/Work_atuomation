import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def click(method, obj):
    aja = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((method, obj)))
    aja.click()

def time_and_close(tickets):
    #iterate list of tickets
    #click them
    #in another tab
    #charge 5 min
    #close them
    #clasify them with glober not answer
    #close tab
    #next
    pass

def close_admin(raw):
    raw = []
    for ticket in raw:
        raw.append(str(ticket.text))
    print(raw)
    pass

def get_mail(web_object):
    raw = str(web_object.text)
    mail = ''

    if "from " in raw:
        mail = raw.split("from ")[1]
    else:
        mail = raw.split("user ")[1]
    print(mail)
    return mail

def write_text(message, box):
    for part in message.split('\n'):
        box.send_keys(part)
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        box.send_keys(Keys.ENTER)

def send_text():
    driver.execute_script("window.open('https://mail.google.com/chat')")
    driver.switch_to.window(driver.window_handles[1])

    chat = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Find people, spaces, and messages']")))

    for mail in mails:
        click(By.XPATH, "//input[@placeholder='Find people, spaces, and messages']")
        chat.send_keys(mail)
        time.sleep(3)
        chat.send_keys(Keys.DOWN)
        chat.send_keys(Keys.ENTER)
        time.sleep(3)
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe[title='Chat content']"))
        click(By.CLASS_NAME, "AYGmkd")
        browser = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "AYGmkd")))
        write_text(message, browser)
        driver.switch_to.parent_frame()


mails = []
message = 'Dear Glober,\n\n We are contacting you because you are trying to validate your Globant account into your device and, accordingly to the new Globant Mobile Device Account Validation Policy informed by GIST, we need to establish an online video-conference (camera must be turned ON) by Google Meet and you must have some ID card with photo to verify your Identity and approve the required access. The meeting will take less than 10 minutes and we will take one screenshot of the session with your face shown.\n\nIf you agree, I’m going to send you the meeting link NOW.\n\nNOTE: We can’t schedule the meeting until next time because this is a “Just in Time” access (that means if you are not available at this moment, we will Delete (Deny) the access until the next time you’ll try to validate the account into your device again).'
options = webdriver.ChromeOptions() 
options.arguments.append('--profile-directory=Profile 1')
options.arguments.append(r"--user-data-dir=C:\Users\Juan\AppData\Local\Google\Chrome\User Data")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://globant.cloud.invgate.net/")
click(By.ID, "button_login")
#enter to requests assigned to me
click(By.ID,"sidebar_requests")
click(By.ID,"tab_562")
click(By.ID,"scroll_button")
time.sleep(1) #if the page does not load before the next line, it wont get all the tickets
raw_tickets = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT,'@globant.com')))

mails = list(map(get_mail, raw_tickets)) #para implementar en admin_ID

for mail in raw_tickets:
    mails.append(get_mail(mail))

click(By.PARTIAL_LINK_TEXT, mails[0])
click(By.ID, 'request_toolbar_time')
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID,'result_time'))).send_keys('5')
click(By.XPATH, "//div[@title='Select a category']")
click(By.XPATH, "//div[@title='Work [Real Time]']")
click(By.CLASS_NAME, 'button-silver')
myelement = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID,'popup_option_yes')))
if myelement.is_displayed():
    myelement.click()
else:
    pass

click(By.ID, 'request_toolbar_menu')
click(By.ID, 'time_solve_action')
click(By.ID, 'popup_option_no')

while True:
    pass
