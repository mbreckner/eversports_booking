import sys
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

from login_flow import execute_login_flow
from setup_driver import setup_chrome_driver

def calculate_wednesday_booking_date():
    today = datetime.now()
    days_until_next_wednesday = (2 - today.weekday() + 7) % 7 + 7  # Move to next Wednesday, then add another week
    next_wednesday_in_two_weeks = today + timedelta(days=days_until_next_wednesday)
    formatted_date_next_wednesday_in_two_weeks = next_wednesday_in_two_weeks.strftime(
        "%d/%m/%Y")  # Format the date as needed
    print("::::: Tries to book a padel court for " + formatted_date_next_wednesday_in_two_weeks)
    return formatted_date_next_wednesday_in_two_weeks
def exit_if_not_thursday():
    current_date = datetime.now()
    if current_date.weekday() == 3:  # Monday is 0, Sunday is 6
        print("::::: Today is Thursday!")
    else:
        print("::::: Today is not Thursday")
def set_datepicker_input():
    formatted_date_next_wednesday_in_two_weeks = calculate_wednesday_booking_date()

    date_picker_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "datepicker"))
    )
    date_picker_input.clear()
    date_picker_input.send_keys(formatted_date_next_wednesday_in_two_weeks)
    date_picker_input.send_keys(Keys.ENTER)
def click_available_timeslot():
    global timeslot_chosen_1900
    global timeslot_chosen_1800
    global timeslot_chosen_2000
    sleep(2)
    try:
        button_timeslot_1900 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_1900_to_book))
        )
        print("::::: 19:00 time slot available")
        timeslot_chosen_1900 = True
        button_timeslot_1900.click()
    except TimeoutException:
        print("::::: 19:00 time slot button not found, searching for an alternative timeslot")
        try:
            button_timeslot_1800 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_1800_to_book))
            )
            print("::::: 18:00 time slot available")
            timeslot_chosen_1800 = True
            button_timeslot_1800.click()
        except TimeoutException:
            print("::::: 18:00 time slot button not found, searching for an alternative timeslot.")
            button_timeslot_2000 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_2000_to_book))
            )
            print("::::: 20:00 time slot available")
            timeslot_chosen_2000 = True
            button_timeslot_2000.click()
def click_padel_tab():
    sleep(2)
    padel_tab = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Padel')]"))
    )
    padel_tab.click()
def adjust_timeframe_to_two_hours():
    open_dropdown_for_timeslot = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='combobox']"))
    )
    open_dropdown_for_timeslot.click()
    timeslot_to_click = ""
    if timeslot_chosen_1900:
        timeslot_to_click = xpath_dropdown_timeslot_end_21_00
    elif timeslot_chosen_1800:
        timeslot_to_click = xpath_dropdown_timeslot_end_20_00
    else:
        timeslot_to_click = xpath_dropdown_timeslot_end_22_00

    try:
        dropdown_menu_2h = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, timeslot_to_click))
        )
        dropdown_menu_2h.click()
        return timeslot_to_click
    except TimeoutException:
        print('::::: ERROR: Booking for 2h not possible, exit')
        sys.exit()
def confirm_booking_and_payment():
    # Select payment method and click 'Pay'
    confirm_payment_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Select payment method']"))
    )
    confirm_payment_button.click()
    pay_now_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Pay now']"))
    )
    pay_now_button.click()

    if timeslot_chosen_1900:
        print('Booked successfully for 19:00-21:00')
    elif timeslot_chosen_1800:
        print('Booked successfully for 18:00-20:00')
    else:
        print('Booked successfully for 20:00-22:00')


eversports_weburl = "https://www.eversports.ch/widget/w/9ckd8j"
login_email = "mbreckner@yahoo.de"
login_password = "HdudYj2WvHhyu8ZHmb"
xpath_for_time_slot_1900_to_book = "//td[@data-original-title='Free | 11:00 - 12:00']"
xpath_dropdown_timeslot_end_21_00 = "//*[text()='13:00']"
xpath_for_time_slot_1800_to_book = "//td[@data-original-title='Free | 18:00 - 19:00']"
xpath_dropdown_timeslot_end_20_00 = "//*[text()='20:00']"
xpath_for_time_slot_2000_to_book = "//td[@data-original-title='Free | 20:00 - 21:00']"
xpath_dropdown_timeslot_end_22_00 = "//*[text()='22:00']"
timeslot_chosen_1900 = False
timeslot_chosen_1800 = False
timeslot_chosen_2000 = False


driver = setup_chrome_driver(True)
exit_if_not_thursday()
driver.get(eversports_weburl)
print("::::: Opened webpage")
execute_login_flow(driver, login_email, login_password)
set_datepicker_input()
click_padel_tab()
click_available_timeslot()
adjust_timeframe_to_two_hours()
confirm_booking_and_payment()

# Close browser
driver.quit()