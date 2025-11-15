import pytest
import time
from Pages.irctc_search_page import IRCTCSearchPage   # REQUIRED
from Utilities.excel_reader import ExcelReader
from Utilities.screenshot_helper import take_screenshot
import os
import allure


class IRCTCSearchPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def handle_popups(self):
        handlers = [
            ("//a[contains(@class,'fa fa-times')]", "Login popup closed"),
            ("//div[contains(@class,'ui-dialog')]//span[contains(@class,'ui-icon-closethick')]", "Promo popup closed"),
            ("//span[contains(text(),'Remove') or contains(text(),'REMOVE')]", "Remove popup closed"),
            ("//button[text()='OK']", "Modal OK handled"),
        ]
        for xpath, msg in handlers:
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                btn.click()
                print(f" {msg}")
                return True
            except TimeoutException:
                continue

        try:
            alert = self.driver.switch_to.alert
            print(f"⚠️ Alert: {alert.text}")
            alert.accept()
            return True
        except NoAlertPresentException:
            pass
        return False

    def enter_from_city(self, short_code, full_name):
        self.handle_popups()
        field = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-controls='pr_id_1_list']")))
        field.click()
        field.clear()
        field.send_keys(short_code)
        time.sleep(1)
        options = self.driver.find_elements(By.XPATH, "//ul[@id='pr_id_1_list']/li/span")
        for opt in options:
            if full_name in opt.text:
                opt.click()
                print(f" From city selected: {opt.text}")
                break
        self.handle_popups()

    def enter_to_city(self, short_code, full_name):
        self.handle_popups()
        field = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-controls='pr_id_2_list']")))
        field.click()
        field.clear()
        field.send_keys(short_code)
        time.sleep(1)
        options = self.driver.find_elements(By.XPATH, "//ul[@id='pr_id_2_list']/li/span")
        for opt in options:
            if full_name in opt.text:
                opt.click()
                print(f" To city selected: {opt.text}")
                break
        self.handle_popups()

    def select_class(self, class_name):
        self.handle_popups()
        dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'All Classes')]")))
        dropdown.click()
        class_xpath = f"//li[contains(@aria-label, '{class_name}')]"
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, class_xpath)))
        option.click()
        print(f"Train class selected: {class_name}")
        self.handle_popups()

    def select_quota(self, quota_name):
        self.handle_popups()
        dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'GENERAL')]")))
        dropdown.click()
        quota_xpath = f"//span[contains(text(),'{quota_name.upper()}')]"
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, quota_xpath)))
        option.click()
        print(f" Quota selected: {quota_name}")
        self.handle_popups()

    def select_railway_pass(self):
        checkbox = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(),'Railway Pass Concession')]/preceding-sibling::input"))
        )
        self.driver.execute_script("arguments[0].click();", checkbox)
        print(" Railway Pass Concession selected")

        ok_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='OK']/parent::button")))
        ok_button.click()
        print(" Concession OK clicked")
        self.handle_popups()

    def click_search(self):
        search_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Search')]")))
        self.driver.execute_script("arguments[0].click();", search_btn)
        print(" Search button clicked")
        self.handle_popups()

    def verify_results(self):
        text = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Results for')]"))).text
        return text

    def get_train_list(self):
        trains = self.driver.find_elements(By.XPATH, "//div[contains(@class,'train-heading')]//strong")
        return [t.text.strip() for t in trains if t.text.strip()]
