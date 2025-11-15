import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time

@pytest.fixture(scope="class")
def setup(request):
    chrome_options = Options()

    # FIX: IRCTC does NOT load properly in --headless=new mode
    chrome_options.add_argument("--headless=chrome")     # ← use this
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # IRCTC-specific fixes
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 40)

    driver.get("https://www.irctc.co.in/nget/train-search")

    # IRCTC takes time to load Angular + popups
    time.sleep(12)

    request.cls.driver = driver
    request.cls.wait = wait

    yield driver, wait
    driver.quit()
