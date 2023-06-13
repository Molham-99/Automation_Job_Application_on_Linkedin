import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
LINKEDIN_URL = os.environ.get("LINKEDIN_URL")
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_driver_path = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=chrome_driver_path, options=chrome_options)
driver.get(f"{LINKEDIN_URL}")
sign_in_button = driver.find_element(by="xpath",
                                     value="/html/body/div[5]/a[1]")
time.sleep(3)
sign_in_button.click()
email_box = driver.find_element(by="id", value="username")
email_box.send_keys(f"{EMAIL}")
email_box = driver.find_element(by="id", value="password")
email_box.send_keys(f"{PASSWORD}")
sign_in_button2 = driver.find_element(by="xpath",
                                     value='//*[@id="organic-div"]/form/div[3]/button')
sign_in_button2.click()
time.sleep(15)


def check(x):
    try:
        check_box = driver.find_element(by='css selector', value='.fb-text-selectable__option label')
        text = driver.find_element(by='css selector', value='.fb-text-selectable__option label').text
        print(text)
        if text == 'Be sure to include an updated resume':
            next_button()
        if text == 'I Agree Terms & Conditions' or text == 'Acknowledge/Confirm':
            print("llll")
            check_box.click()
        address = driver.find_element(by="css selector", value='.relative label').text
        if address == 'City':
            city_box = driver.find_element(by="css selector", value='.search-basic-typeahead input')
            city_box.send_keys("Prague 5, Prague, Czechia")
            x.click()
            next_button()
        work_experience = driver.find_element(by="css selector",
                                              value='.artdeco-text-input--container label').text
        if work_experience == 'How many years of work experience do you have with Python (Programming Language)?':
            next = driver.find_elements(by="css selector", value='.display-flex button')
            for o in next:
                y = o.get_attribute("aria-label")
                if y == "Review your application":
                    o.click()
        additional = driver.find_element(by='css selector', value='.pb4 h3').text
        # print(additional)
        if additional == 'Additional Questions':
            # print(additional)
            discard()
        if text == 'Yes':
            discard()
        hear_about_job = driver.find_element(by="css selector", value='.artdeco-text-input--container label').text
        if hear_about_job == 'How did you hear about this job?':
            text_linkedin = driver.find_element(by='css selector', value='.artdeco-text-input--container input')
            text_linkedin.send_keys("Linkedin")
    except NoSuchElementException:
        pass
    except ElementClickInterceptedException or StaleElementReferenceException:
        pass


def next_button():
    time.sleep(1)
    next_button_aria_label = driver.find_elements(by='css selector', value='.display-flex button')
    for x in next_button_aria_label:
        y = x.get_attribute("aria-label")
        if y == "Submit application":
            x.click()
            time.sleep(2)
            close = driver.find_element(by='css selector', value='.artdeco-modal-overlay button')
            close.click()
            break
        elif y == "Continue to next step":
            x.click()
            check(x)
            next_button()
        elif y == "Review your application":
            x.click()
            check(x)
            discard()
        else:
            pass


def discard():
    close = driver.find_element(by='css selector', value='button')
    close.click()
    time.sleep(2)
    discard = driver.find_element(by='css selector', value='.artdeco-modal__actionbar button')
    discard.click()


def apply():
    try:
        apply_button = driver.find_element(by="css selector", value='.jobs-apply-button--top-card')
        apply_button.click()
        time.sleep(1)
        job_header = driver.find_element(by="id", value='jobs-apply-header').text
        time.sleep(1)
        if job_header != 'Apply to Accolade, Inc.':
            next_button()
        else:
            discard()
    except NoSuchElementException:
        pass


def opportunities_list():
    time.sleep(10)
    first_opportunity = driver.find_elements(by="css selector",
                                             value='.scaffold-layout__list-container li')
    jobs_id = []
    for x in first_opportunity:
        id = x.get_attribute("id")
        if id != '':
            jobs_id.append(id)
    print(jobs_id)
    for id in jobs_id:
        print(id)
        button = driver.find_element(by="id", value=f"{id}")
        time.sleep(3)
        button.click()
        time.sleep(3)
        apply()


pages = driver.find_elements(by='css selector', value='.jobs-search-results-list__pagination button')
for page in pages:
    page.click()
    opportunities_list()
