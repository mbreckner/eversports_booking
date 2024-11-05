from time import sleep
import sys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

xpath_for_time_slot_1800_to_book = "//td[@data-original-title='Free | 18:00 - 19:00']"
xpath_for_time_slot_1900_to_book = "//td[@data-original-title='Free | 19:00 - 20:00']"
xpath_for_time_slot_2000_to_book = "//td[@data-original-title='Free | 20:00 - 21:00']"
xpath_for_time_slot_2100_to_book = "//td[@data-original-title='Free | 21:00 - 22:00']"

def select_booking_slot(driver):
    try:
        select_19_to_21(driver)
        print("::::: 19:00-21:00 is available")

    except TimeoutException:
        print("::::: 19:00-21:00 is not available, search for another slot")
        try:
            select_20_to_22(driver)
            print("::::: 20:00-22:00 is available")
        except TimeoutException:
            print("::::: 20:00-22:00 is not available, search for another slot")
            try:
                select_18_to_20(driver)
                print("::::: 18:00-20:00 is available")
            except TimeoutException:
                print("::::: ERROR: 18:00-20:00 is not available, exit")
                sys.exit(1)
    continue_to_checkout(driver)

def select_19_to_21(driver):
    slot_19_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_1900_to_book))
    )
    slot_20_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_2000_to_book))
    )
    slot_19_button.click()
    slot_20_button.click()

def select_20_to_22(driver):
    slot_20_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_2000_to_book))
    )
    slot_21_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_2100_to_book))
    )
    slot_20_button.click()
    slot_21_button.click()

def select_18_to_20(driver):
    slot_18_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_1800_to_book))
    )
    slot_19_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_1900_to_book))
    )
    slot_18_button.click()
    slot_19_button.click()

def continue_to_checkout(driver):
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Continue to Checkout']"))
    )
    continue_button.click()