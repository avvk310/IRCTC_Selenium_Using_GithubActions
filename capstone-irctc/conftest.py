import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import os

@pytest.fixture(scope="class")
def setup(request):
    chrome_options = Options()

    # IMPORTANT: No headless for IRCTC
    # Chrome runs inside Xvfb display :99
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    # ---- Required for CI (GitHub Actions) ----
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--display=:99")

    # prevent IRCTC anti-automation detection
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 40)

    driver.set_window_size(1920, 1080)

    driver.get("https://www.irctc.co.in/nget/train-search")

    time.sleep(8)  # allow IRCTC JS + Angular load

    request.cls.driver = driver
    request.cls.wait = wait

    yield driver, wait
    driver.quit()
