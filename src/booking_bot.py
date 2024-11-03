from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
from webdriver_manager.chrome import ChromeDriverManager
import sys
import time

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless
chrome_options.add_argument("--no-sandbox")  # Overcome limited resource problems
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Initialize the Chrome driver with the options
chrome_version = "114.0.5735.90-1"  # This should match the version of Chromium you have
service = Service(ChromeDriverManager(chrome_version).install())
driver = webdriver.Chrome(service=service, options=chrome_options)

########## Pre 1. Finish if it's not Wednesday
current_date = datetime.now()
# Check if the current day is Wednesday
if current_date.weekday() == 3:  # Monday is 0, Sunday is 6
    print("Today is Thursday!")
else:
    print("Today is not Thursday")
    '''sys.exit()'''


########## Pre 2. Setup variables
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

########## 1. Set up Selenium and access the website
#driver = webdriver.Chrome()  # Make sure to specify the path if necessary
driver.get("https://www.eversports.ch/widget/w/9ckd8j")



########## 2. Login
### Go to login mask and select 'Continue with google'
openLoginPageButton = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[text()='Login / Register']"))
)
openLoginPageButton.click()

acceptCookieButton = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[text()='Accept all']"))
)
acceptCookieButton.click()

# Find and fill in login fields
driver.find_element(By.XPATH, "//input[@type='email']").send_keys(login_email)
driver.find_element(By.XPATH, "//input[@type='password']").send_keys(login_password)
confirmLoginFormButton = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='login']"))
)
confirmLoginFormButton.click()


########## 3. Set the booking date to next Wednesday
# calculate the next wednesday in two weeks
sleep(2)
today = datetime.now()
days_until_next_wednesday = (2 - today.weekday() + 7) % 7 + 7  # Move to next Wednesday, then add another week
next_wednesday_in_two_weeks = today + timedelta(days=days_until_next_wednesday)
formatted_date_next_wednesday_in_two_weeks = next_wednesday_in_two_weeks.strftime("%d/%m/%Y")  # Format the date as needed
print("Tries to book a padel court for " + formatted_date_next_wednesday_in_two_weeks)

# set date to datepicker and clicks ENTER
datePickerInput = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "datepicker"))
)
datePickerInput.clear()
datePickerInput.send_keys(formatted_date_next_wednesday_in_two_weeks)
datePickerInput.send_keys(Keys.ENTER)


########## 4. Navigate to the Padel court booking section
sleep(2)
padelTab = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Padel')]"))
)
padelTab.click()


########## 5. Select time slot and confirm booking, first try 19:00, then 18:00, then 20:00
sleep(2)
try:
    button_timeslot_1900 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_1900_to_book))
    )
    print("19:00 time slot available")
    timeslot_chosen_1900 = True
    button_timeslot_1900.click()
except TimeoutException:
    print("19:00 time slot button not found, searching for an alternative timeslot")
    try:
        button_timeslot_1800 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_1800_to_book))
        )
        print("18:00 time slot available")
        timeslot_chosen_1800 = True
        button_timeslot_1800.click()
    except TimeoutException:
        print("18:00 time slot button not found, searching for an alternative timeslot.")
        button_timeslot_2000 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_for_time_slot_2000_to_book))
        )
        print("20:00 time slot available")
        timeslot_chosen_2000 = True
        button_timeslot_2000.click()

'''
########## 6. In Booking Page: Adjust time slot to 2h
open_dropdown_for_timeslot = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@role='combobox']"))
)
open_dropdown_for_timeslot.click()
timeslot_to_click = "a"
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
except TimeoutException:
    print('Booking for 2h not possible, exit')
    sys.exit()
'''

# Optional: Screenshot for confirmation
#driver.save_screenshot("eversports_booking_confirmation.png")

# Select payment method and click 'Pay'
confirm_payment_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Select payment method']"))
    )
confirm_payment_button.click()
time.sleep(4)

# Optional: Screenshot for confirmation
#driver.save_screenshot("eversports_booking_confirmation.png")
if timeslot_chosen_1900:
    timeslot_to_click = xpath_dropdown_timeslot_end_21_00
    print('Booked successfully for 19:00-21:00')
elif timeslot_chosen_1800:
    timeslot_to_click = xpath_dropdown_timeslot_end_20_00
    print('Booked successfully for 18:00-20:00')
else:
    timeslot_to_click = xpath_dropdown_timeslot_end_22_00
    print('Booked successfully for 20:00-22:00')

# Close browser
driver.quit()