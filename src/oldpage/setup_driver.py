import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

def setup_chrome_driver(is_headless):
    chromedriver_autoinstaller.install()
    chrome_options = get_chrome_options(is_headless)
    # driver = webdriver.Chrome(options=chrome_options)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_chrome_options(is_headless):
    if is_headless:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless
        chrome_options.add_argument("--no-sandbox")  # Overcome limited resource problems
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("window-size=1920,1080")  # Set screen size to avoid issues in headless mode
        return chrome_options
    else:
        return Options()
