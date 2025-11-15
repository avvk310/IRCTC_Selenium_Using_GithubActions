import os
import time

def take_screenshot(driver, name="screenshot"):
    """Takes a screenshot and saves it under Reports/screenshots with timestamp"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshots_dir = os.path.join(os.getcwd(), "Reports", "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    file_path = os.path.join(screenshots_dir, f"{name}_{timestamp}.png")
    driver.save_screenshot(file_path)
    print(f"📸 Screenshot saved: {file_path}")
    return file_path
