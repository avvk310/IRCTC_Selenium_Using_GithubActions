import pytest
import time
import Pages.irctc_search_page
from Utilities.excel_reader import ExcelReader
from Utilities.screenshot_helper import take_screenshot
import allure
import os
# Load Excel data
excel_path = os.path.join(os.getcwd(), "TestData", "TestData.xlsx")
excel = ExcelReader(excel_path)
bus_data = excel.get_data("Sheet1")

@pytest.mark.usefixtures("setup")
class TestIRCTCSearch:
    @pytest.mark.parametrize("data", bus_data)
    def test_irctc_train_search(self, setup, data):
        # ⚡ Declare irctc INSIDE the function
        driver, wait = setup
        irctc = IRCTCSearchPage(driver, wait)

        from_city = data["from_city"]
        to_city = data["to_city"]
        train_class = data["class"]
        quota = data["quota"]

        print(f"\n Searching trains from '{from_city}' to '{to_city}' | Class: {train_class} | Quota: {quota}")

        irctc.handle_popups()
        irctc.enter_from_city(from_city.split('-')[0].strip(), from_city)
        irctc.enter_to_city(to_city.split('-')[0].strip(), to_city)
        irctc.select_class(train_class)
        irctc.select_quota(quota)
        irctc.click_search()

        # Take screenshot
        take_screenshot(driver, name=f"{from_city.split()[0]}_to_{to_city.split()[0]}")

        trains = irctc.get_train_list()
        print(f" Total trains: {len(trains)}")
        for i, t in enumerate(trains, 1):
            print(f"{i}. {t}")

        assert len(trains) > 0, "No trains found for this route!"
        # Ensure reports folder exists
        os.makedirs("./reports", exist_ok=True)
