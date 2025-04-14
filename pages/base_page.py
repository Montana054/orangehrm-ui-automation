import time
import os
import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import logger



class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.img_before_src = None

    DASHBOARD_LABEL = (By.XPATH, "//h6[text()='Dashboard']")
    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='Username']")

    @allure.step("Click element: {locator}")
    def click(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            logger.info(f"Clicking element: {locator}")
            element.click()
        except Exception as e:
            logger.error(f"🚨 Click failed for {locator}: {e}")
            raise

    @allure.step("Upload profile picture")
    def upload_profile_picture(self, profile_locator, upload_locator, image_path=None):
        if "GITHUB_ACTIONS" in os.environ:
            logger.info("📷 Skipping profile upload in CI")
            return
        if not image_path:
            image_path = r"C:\PythonTesting\orangeHrmLive\test_data\employee_200_200.jpg"
        img_element = self.wait.until(EC.presence_of_element_located(profile_locator))
        self.img_before_src = img_element.get_attribute("src")
        upload_input = self.wait.until(EC.presence_of_element_located(upload_locator))
        upload_input.send_keys(image_path)
        self.wait.until(lambda d: img_element.get_attribute("src") != self.img_before_src)
        logger.info("✅ Profile picture uploaded successfully")

    def is_profile_picture_updated(self, locator):
        img_element = self.wait.until(EC.presence_of_element_located(locator))
        img_after_src = img_element.get_attribute("src")
        updated = self.img_before_src != img_after_src

        if updated:
            logger.info("✅ Profile picture updated successfully")
        else:
            logger.error("❌ Profile picture was NOT updated")

        return updated

    @allure.step("Enter text '{text}' into {locator}")
    def send_keys(self, locator, text, clear_first=True):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            logger.info(f"Entering text '{text}' into: {locator}")
            if clear_first:
                element.clear()
            if text:
                element.send_keys(text)
        except Exception as e:
            logger.error(f"🚨 Send_keys failed for {locator}: {e}")
            raise

    @allure.step("Force clear and enter text '{text}' into {locator}")
    def send_keys_force_clear(self, locator, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            logger.info(f"Force clearing and entering text '{text}' into: {locator}")
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.BACKSPACE)
            element.send_keys(text)
        except Exception as e:
            logger.error(f"🚨 Send_keys_force_clear failed for {locator}: {e}")
            raise


    def wait_until_presence_of_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Get logged-in username from user dropdown")
    def get_logged_in_username(self):
        try:
            dropdown = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "oxd-userdropdown-name")))
            username = dropdown.text.strip()
            logger.info(f"👤 Logged in username: {username}")
            return username
        except Exception as e:
            logger.error(f"❌ Failed to get logged in username: {e}")
            return None



    @allure.step("Wait until element is visible: {locator}")
    def wait_until_visibility_of_element(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception as e:
            logger.warning(f"⚠️ Element {locator} not visible: {e}")
            return False

    @allure.step("Get text from element: {locator}")
    def get_element_text(self, locator):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text
            logger.info(f"Retrieved text: '{text}'")
            return text.strip()
        except Exception as e:
            logger.error(f"🚨 get_element_text failed: {e}")
            return None

    @allure.step("Check if message is displayed: '{expected_text}'")
    def is_message_displayed(self, locator, expected_text, timeout=5):
        """Universal method for checking notification text (toasters, etc.)"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            element = self.wait.until(EC.presence_of_element_located(locator))
            actual_text = element.text.strip()
            logger.info(f"🔍 Checking message: Expected '{expected_text}', Actual '{actual_text}'")
            return expected_text in actual_text
        except Exception as e:
            logger.error(f"🚨 Failed to find or check message: {e}")
            return False

    @allure.step("Scroll to element: {locator}")
    def scroll_to_element(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            logger.info(f"✅ Scrolled to element: {locator}")
        except Exception as e:
            logger.error(f"🚨 scroll_to_element failed: {e}")
            raise

    @allure.step("Check if user is logged in")
    def is_employee_logged_in(self):
        try:
            dashboard_locator = getattr(self, "DASHBOARD_LABEL", None)
            if not dashboard_locator:
                raise AttributeError("DASHBOARD_LABEL not found in Page Object")
            self.wait.until(EC.presence_of_element_located(dashboard_locator))
            return True
        except Exception as e:
            logger.error(f"🚨 is_logged_in: Entrance check failed: {e}")
            return False

    @allure.step("Check if user is logged out")
    def is_logged_out(self):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
            return element.is_displayed()
        except Exception as e:
            logger.error(f"🚨 is_logged_out check failed: {e}")
            return False

    @allure.step("Select '{option_text}' from dropdown '{label_text}'")
    def select_dropdown_by_label(self, label_text, option_text, listbox_locator, option_locator, fail_if_missing=True):
        try:
            dropdown_locator = (By.XPATH, f"//label[text()='{label_text}']/following::div[1]")
            dropdown = self.wait.until(EC.element_to_be_clickable(dropdown_locator))
            dropdown.click()

            self.wait.until(EC.presence_of_element_located(listbox_locator))

            try:
                self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "oxd-form-loader")))
            except Exception:
                logger.info("⚠️ No loader appeared — continuing")

            options = self.wait.until(EC.presence_of_all_elements_located(option_locator))
            for option in options:
                if option.text.strip() == option_text:
                    try:
                        option.click()
                    except Exception as click_error:
                        logger.warning(f"⚠️ Initial click failed, retrying: {click_error}")
                        time.sleep(0.5)
                        option.click()

                    logger.info(f"🟢 Selected '{option_text}' from dropdown '{label_text}'")
                    return

            message = f"⚠️ Option '{option_text}' not found in dropdown '{label_text}'"
            if fail_if_missing:
                logger.error(f"❌ {message}")
                raise Exception(message)
            else:
                logger.warning(message + ". Continuing without selection.")
                return

        except Exception as e:
            logger.error(f"🚨 Failed to select option '{option_text}' in dropdown '{label_text}': {e}")
            if fail_if_missing:
                raise

    @allure.step("Find employee in table by ID: {employee_id}")
    def find_employee_in_table_by_id(self, employee_id, employee_table, employee_rows):
        try:
            self.wait.until(EC.presence_of_element_located(employee_table))
            self.wait.until(lambda d: len(d.find_elements(*employee_rows)) > 0)

            rows = self.driver.find_elements(*employee_rows)
            logger.info(f"🔍 Searching for employee ID: {employee_id} among {len(rows)} rows")

            for row in rows:
                row_text = row.text.strip()
                logger.debug(f"Checking row: {repr(row_text)}")
                if employee_id in row_text:
                    logger.info(f"✅ Employee found: {employee_id}")
                    row.click()
                    return True

            logger.error(f"❌ Employee with ID {employee_id} not found in table")
            return False

        except Exception as e:
            logger.error(f"🚨 Error while searching for employee in table: {e}")
            raise


