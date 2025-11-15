import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time

@pytest.fixture(scope="class")
def setup(request):
    chrome_options = Options()

    # Required for GitHub Actions headless execution
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # IRCTC-specific fixes (Angular heavy site)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Your original settings
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)   # Increased timeout for IRCTC

    # Load IRCTC website
    driver.get("https://www.irctc.co.in/nget/train-search")

    # IRCTC takes time to fully load UI in headless mode
    time.sleep(8)

    request.cls.driver = driver
    request.cls.wait = wait

    yield driver, wait
    driver.quit()
