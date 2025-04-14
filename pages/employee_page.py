
from pages.base_page import BasePage
import allure

from selenium.webdriver.common.by import By

from pages.main_page import MainPage
from utils.logger import logger


class EmployeePage(BasePage):

    ADMIN_LABEL = (By.XPATH, "//span[normalize-space()='Admin']")

    @allure.step("Checking if employee is logged in (by displayed name)")
    def is_employee_logged_in(self, expected_name: str):
        logger.info("🔍 Checking if logged-in employee name matches expected")
        actual_name = self.get_logged_in_username()
        if actual_name is None:
            logger.warning("⚠️ Could not retrieve logged-in username")
            return False
        match = actual_name == expected_name
        logger.info(f"✅ Username match: {match} (expected: '{expected_name}', actual: '{actual_name}')")
        return match

    @allure.step("Logging out as employee")
    def logout_employee(self):
        try:
            logger.info("🔚 Logging out as employee")
            self.click(MainPage.USER_DROPDOWN)
            self.click(MainPage.LOGOUT_BUTTON)
        except Exception as e:
            logger.warning(f"⚠️ Logout failed for employee: {e}")
