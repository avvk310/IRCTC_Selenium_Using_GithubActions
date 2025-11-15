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
        popup_xpaths = [
            "//button[contains(text(),'OK')]",
            "//span[contains(text(),'OK')]/parent::button",
            "//a[contains(@class,'fa fa-times')]",
            "//span[contains(@class,'ui-icon-closethick')]",
            "//div[contains(@class,'ui-dialog')]//button",
            "//button[contains(text(),'Dismiss')]",
            "//button[contains(text(),'close') or contains(text(),'Close')]",
            "//span[contains(text(),'×')]",
            "//div[@role='dialog']//button",
        ]

        for xpath in popup_xpaths:
            try:
                btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(1)
                print(f"[Popup Closed] {xpath}")
            except:
                continue

        # Also remove transparent backdrop blocking clicks
        try:
            self.driver.execute_script("""
                const backdrops = document.querySelectorAll('.cdk-overlay-backdrop');
                backdrops.forEach(b => b.style.display = 'none');
            """)
        except:
            pass

        return True

    # -----------------------------------------------------------
    # ✔ UPDATED METHOD — robust for GitHub Actions + Xvfb
    # -----------------------------------------------------------
    def enter_from_city(self, short_code, full_name):

        self.handle_popups()

        # Remove Angular overlays
        self.driver.execute_script("""
            const backdrops = document.querySelectorAll('.cdk-overlay-backdrop');
            backdrops.forEach(b => b.style.display = 'none');
        """)

        # ⚠️ FULL fallback list including CI locator
        fallback_locators = [
            "//input[@id='origin']",  # GitHub Actions layout
            "//input[@aria-controls='pr_id_1_list']",  # Normal IRCTC layout
            "//input[contains(@placeholder,'From')]",  # Alternate layout
            "//input[contains(@aria-label,'From')]",  # Mobile layout
            "//input[@type='text' and contains(@class,'ui-inputtext')]"  # Generic fallback
        ]

        field = None
        for xpath in fallback_locators:
            try:
                field = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                # bring into view
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", field)
                time.sleep(0.5)
                break
            except:
                field = None
                continue

        if not field:
            # DEBUG: capture page source for analysis
            with open("/tmp/irctc_debug_from_input.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            self.driver.save_screenshot("/tmp/irctc_debug_from_input.png")
            raise TimeoutException("From city input field not found in CI environment.")

        # Type short code
        try:
            field.click()
            field.clear()
            field.send_keys(short_code)
            time.sleep(2)
        except:
            # fallback send via JS
            self.driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', {bubbles:true}));
            """, field, short_code)
            time.sleep(2)

        # Select option from dropdown
        options = self.driver.find_elements(By.XPATH, "//ul[contains(@id,'pr_id')]/li/span")
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
