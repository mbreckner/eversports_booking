from time import sleep
import sys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def execute_login_flow(driver, login_email_text, login_password_text):
    try:
        accept_cookies(driver)
        open_login_page(driver)
        enter_email_and_password(driver, login_email_text, login_password_text)
        confirm_login(driver)
        click_book_now(driver)
        print("::::: Login successfull")

    except TimeoutException:
        print("::::: ERROR:Timeout in login flow")
        sys.exit(1)


def open_login_page(driver):
    open_login_button_xpath = "//*[text()='Login']"
    open_login_page_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, open_login_button_xpath))
    )
    open_login_page_button.click()

def accept_cookies(driver):
    accept_cookie_button_xpath = "//*[text()='Accept all']"
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, accept_cookie_button_xpath))
    )
    accept_cookie_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, accept_cookie_button_xpath))
    )
    accept_cookie_button.click()

def enter_email_and_password(driver, login_email_text, login_password_text):
    sleep(1)
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(login_email_text)
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys(login_password_text)

def confirm_login(driver):
    confirm_login_form_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='login']"))
    )
    confirm_login_form_button.click()

def click_book_now(driver):
    book_now_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Book Now']"))
    )
    book_now_button.click()