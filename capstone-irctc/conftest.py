import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

@pytest.fixture(scope="class")
def setup(request):
    chrome_options = Options()

    # ❌ DO NOT USE HEADLESS (IRCTC WILL NOT LOAD)
    # chrome_options.add_argument("--headless")

    # Tell Chrome to use the Xvfb virtual display
    chrome_options.add_argument("--display=:99")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # IRCTC specific stabilization
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 40)

    driver.get("https://www.irctc.co.in/nget/train-search")

    time.sleep(10)

    request.cls.driver = driver
    request.cls.wait = wait

    yield driver, wait
    driver.quit()
