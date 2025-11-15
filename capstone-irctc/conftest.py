import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time

@pytest.fixture(scope="class")
def setup(request):
    chrome_options = Options()

    # REQUIRED TO BYPASS IRCTC BOT DETECTION
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Spoof real user agent (very important)
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.5993.90 Safari/537.36"
    )

    # GitHub Actions Display
    chrome_options.add_argument("--display=:99")
    chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")

    # Create driver
    driver = webdriver.Chrome(options=chrome_options)

    # Remove navigator.webdriver flag (MOST IMPORTANT)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    wait = WebDriverWait(driver, 40)

    driver.get("https://www.irctc.co.in/nget/train-search")

    time.sleep(5)

    request.cls.driver = driver
    request.cls.wait = wait

    yield driver, wait
    driver.quit()
