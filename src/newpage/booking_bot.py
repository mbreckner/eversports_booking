from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

from login_flow import execute_login_flow
from setup_driver import setup_chrome_driver
from select_booking_slot import select_booking_slot

def calculate_wednesday_booking_date():
    #wednesday_day_of_the_week = 2
    wednesday_day_of_the_week = 0
    today = datetime.now()
    days_until_next_wednesday = (wednesday_day_of_the_week - today.weekday() + 7) % 7 + 7  # Move to next Wednesday, then add another week
    next_wednesday_in_two_weeks = today + timedelta(days=days_until_next_wednesday)
    formatted_date_next_wednesday_in_two_weeks = next_wednesday_in_two_weeks.strftime(
        "%d/%m/%Y")  # Format the date as needed
    print("::::: Tries to book a padel court for " + formatted_date_next_wednesday_in_two_weeks)
    return formatted_date_next_wednesday_in_two_weeks
def set_datepicker_input():
    formatted_date_next_wednesday_in_two_weeks = calculate_wednesday_booking_date()

    date_picker_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "datepicker"))
    )
    date_picker_input.clear()
    date_picker_input.send_keys(formatted_date_next_wednesday_in_two_weeks)
    date_picker_input.send_keys(Keys.ENTER)
def click_padel_tab():
    sleep(2)
    padel_tab = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Padel')]"))
    )
    padel_tab.click()
def confirm_booking_and_payment():
    # Select payment method and click 'Pay'
    confirm_payment_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Select payment method']"))
    )
    confirm_payment_button.click()
    pay_now_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Pay now']"))
    )
    if prod_run:
        pay_now_button.click()
        sleep(20)
    else:
        print('::::: !!!TEST RUN!!!')
        sleep(5)

    if timeslot_chosen_1900:
        print('::::: Booked successfully for 19:00-21:00')
    elif timeslot_chosen_1800:
        print('::::: Booked successfully for 18:00-20:00')
    else:
        print('::::: Booked successfully for 20:00-22:00')

is_headless = False
prod_run = True
eversports_weburl = "https://www.eversports.ch/s/oro-sportcenter"
login_email = "mbreckner@yahoo.de"
login_password = "HdudYj2WvHhyu8ZHmb"
xpath_for_time_slot_1900_to_book = "//td[@data-original-title='Free | 19:00 - 20:00']"
xpath_dropdown_timeslot_end_21_00 = "//*[text()='21:00']"
xpath_for_time_slot_1800_to_book = "//td[@data-original-title='Free | 18:00 - 19:00']"
xpath_dropdown_timeslot_end_20_00 = "//*[text()='20:00']"
xpath_for_time_slot_2000_to_book = "//td[@data-original-title='Free | 20:00 - 21:00']"
xpath_dropdown_timeslot_end_22_00 = "//*[text()='22:00']"
timeslot_chosen_1900 = False
timeslot_chosen_1800 = False
timeslot_chosen_2000 = False


driver = setup_chrome_driver(is_headless)
driver.get(eversports_weburl)
print("::::: Opened webpage")
execute_login_flow(driver, login_email, login_password)
set_datepicker_input()
click_padel_tab()
select_booking_slot(driver)
confirm_booking_and_payment()

# Close browser
driver.quit()