import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger
import allure

class LoginPage(BasePage):


    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='Username']") # username
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Password']") # password
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'oxd-alert-content-text')]")

    @allure.step("Logging in as {username}")
    def login(self, username, password):
        try:
            logger.info(f"🔐 Attempting to log in as: {username}")
            self.send_keys(self.USERNAME_INPUT, username)
            self.send_keys(self.PASSWORD_INPUT, password)
            self.click(self.LOGIN_BUTTON)
            logger.info("✅ Login action completed.")
        except Exception as e:
            logger.error(f"🚨 Login failed! Error: {e}")
            pytest.fail(f"❌ TEST FAILED in login(): {e}")

    @allure.step("Getting error message")
    def get_error_message(self):
        logger.info("ℹ️ Retrieving error message from the page.")
        error_locator = self.ERROR_MESSAGE
        return self.get_element_text(error_locator)




