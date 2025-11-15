# capstone-irctc/Pages/irctc_search_page.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

class IRCTCSearchPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def handle_popups(self):
        try:
            # Remove Angular CDK overlays completely
            self.driver.execute_script("""
                document.querySelectorAll('.cdk-overlay-container, .cdk-overlay-backdrop')
                .forEach(e => e.remove());
            """)
        except:
            pass

        # Try clicking visible close buttons
        popup_xpaths = [
            "//button[contains(text(),'OK')]",
            "//span[contains(@class,'ui-icon-closethick')]",
            "//a[contains(@class,'fa fa-times')]",
            "//span[contains(text(),'Remove') or contains(text(),'REMOVE')]"
        ]

        for xp in popup_xpaths:
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(1)
            except:
                continue

        # try closing alerts
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            pass

    # -----------------------------------------------------------
    # ✔ UPDATED METHOD — robust for GitHub Actions + Xvfb
    # -----------------------------------------------------------
    def enter_from_city(self, short_code, full_name):

        self.handle_popups()

        # Remove Angular overlays (very important for CI)
        self.driver.execute_script("""
            document.querySelectorAll('.cdk-overlay-backdrop')
            .forEach(e => e.style.display='none');
        """)

        # --- FULL LIST FOR ALL IRCTC LAYOUTS (Local + CI) ---
        fallback_locators = [
            "//input[@id='input-from']",  # CI version
            "//input[@formcontrolname='origin']",  # CI alt
            "//input[@id='origin']",  # mobile UI
            "//input[@aria-controls='pr_id_1_list']",  # normal UI
            "//input[contains(@placeholder,'From')]",  # fallback
            "//input[contains(@aria-label,'From')]",  # fallback
            "//input[@type='text' and contains(@class,'ui-inputtext')]"  # last fallback
        ]

        field = None

        for xpath in fallback_locators:
            try:
                field = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", field
                )
                time.sleep(1)
                break
            except Exception:
                field = None
                continue

        if not field:
            # DEBUG files for GitHub
            with open("/tmp/irctc_debug_from_input.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.driver.save_screenshot("/tmp/irctc_debug_from_input.png")
            raise TimeoutException("From city input field not found (CI mode).")

        # --- TYPE SHORT CODE ---
        try:
            field.click()
            field.clear()
            field.send_keys(short_code)
            time.sleep(2)
        except Exception:
            # If typing fails → use JS
            self.driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', {bubbles:true}));
            """, field, short_code)
            time.sleep(2)

        # --- SELECT DROPDOWN RESULT ---
        options = self.driver.find_elements(By.XPATH, "//li//span")
        for opt in options:
            if full_name in opt.text:
                opt.click()
                print("From city selected:", opt.text)
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
