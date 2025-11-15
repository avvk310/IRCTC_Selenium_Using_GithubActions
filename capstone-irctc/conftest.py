import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture(scope="class")
def setup(request):
    chrome_options = Options()

    # IMPORTANT: DO NOT USE HEADLESS (IRCTC blocks headless Chrome)
    # chrome_options.add_argument("--headless")

    # Xvfb already sets DISPLAY=:99 in GitHub Actions
    # DO NOT ADD chrome_options.add_argument("--display=:99")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Anti-bot detection bypass
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    # Start Chrome
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 40)

    # IRCTC loads slowly in GitHub Actions → require extra time
    driver.get("https://www.irctc.co.in/nget/train-search")
    time.sleep(10)

    request.cls.driver = driver
    request.cls.wait = wait

    yield driver, wait
    driver.quit()
