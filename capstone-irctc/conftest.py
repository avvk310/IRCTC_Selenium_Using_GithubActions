import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time

@pytest.fixture(scope="class")
def setup(request):
    chrome_options = Options()

    # REQUIRED FOR GITHUB ACTIONS (headless Linux)
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Your original options (optional)
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.irctc.co.in/nget/train-search")
    time.sleep(3)

    request.cls.driver = driver
    request.cls.wait = wait

    yield driver, wait
    driver.quit()
