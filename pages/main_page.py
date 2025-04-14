from selenium.webdriver.common.by import By
from  pages.base_page import BasePage
from utils.logger import logger
import allure
from utils.data_helper import generate_unique_employee_id, generate_unique_username
from utils.data_helper import save_employee_to_csv


class MainPage(BasePage):

    USER_DROPDOWN = (By.CLASS_NAME, "oxd-userdropdown-tab")
    LOGOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Logout')]")
    PIM_TAB = (By.XPATH, "//span[text()='PIM']")
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")
    FIRST_NAME = (By.CSS_SELECTOR, "input[placeholder='First Name']") # First name
    LAST_NAME = (By.CSS_SELECTOR, "input[placeholder='Last Name']")
    EMPLOYEE_ID = (By.XPATH, "//label[text()='Employee Id']/following::input[1]")
    ENABLE_LOGIN_TOGGLE = (By.XPATH, "//span[contains(@class, 'oxd-switch-input')]")
    USERNAME_FIELD = (By.XPATH, "//label[text()='Username']/following::input[1]")
    PASSWORD_FIELD = (By.XPATH, "//label[text()='Password']/following::input[1]")
    CONFIRM_PASSWORD_FIELD = (By.XPATH, "//label[text()='Confirm Password']/following::input[1]")
    PROFILE_PICTURE = (By.XPATH, "//img[contains(@class, 'employee-image')]")
    UPLOAD_INPUT_PIC = (By.XPATH, "//input[@type='file']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    TOASTER_SUCCESS_MESSAGE = (By.ID, "oxd-toaster_1")
    SUCCESS_MESSAGE = (By.ID, "oxd-toaster_1")
    ERROR_MESSAGE = (By.XPATH, "//div[@class='alert alert-danger']")
    LICENSE_NUMBER_LABEL = (By.XPATH, "//label[text()=\"Driver's License Number\"]/following::input[1]") # //label[text()=\"Drivers License Number\"]/following::input[1]
    LICENSE_EXP_LABEL = (By.XPATH, "//label[text()=\"License Expiry Date\"]/following::input[1]")
    DROPDOWN_LISTBOX = (By.XPATH, "//div[@role='listbox']")
    DROPDOWN_OPTIONS = (By.XPATH, "//div[@role='option']")
    DATE_OF_BIRTH_LABEL = (By.XPATH, "//label[text()='Date of Birth']/following::input[1]")
    MALE_LABEL = (By.XPATH, "//label[text()='Male']")
    SUBMIT_BUTTON_TYPE = (By.CSS_SELECTOR, "div[class='orangehrm-horizontal-padding orangehrm-vertical-padding'] button[type='submit']")
    JOB_TAB = (By.XPATH, "//a[normalize-space()='Job']")
    JOINED_DATE_LABEL = (By.XPATH, "//label[text()='Joined Date']/following::input[1]")
    EMPLOYEE_TABLE = (By.XPATH, "//div[@class='oxd-table-body']")
    EMPLOYEE_ROWS = (By.XPATH, "//div[@class='oxd-table-card']")
    DASHBOARD_LABEL = (By.XPATH, "//h6[text()='Dashboard']")

    @allure.step("Create employee user only (light version)")
    def create_employee_user(self, first_name="Alexandr", last_name="Petrov"):
        logger.info("🟢 Creating employee user only (without profile details)")
        employee_id, username = self.fill_basic_info(first_name, last_name)
        save_employee_to_csv(username, employee_id)
        logger.info("✅ Employee user saved to CSV: %s / %s", username, employee_id)
        return username

    @allure.step("Logout from system")
    def logout(self):
        try:
            logger.info("🔚 Logging out")
            self.click(self.USER_DROPDOWN)
            self.click(self.LOGOUT_BUTTON)
        except Exception as e:
            logger.warning(f"⚠️ Logout failed or user was already logged out: {e}")

    @allure.step("Filling basic information (name, login, password)")
    def fill_basic_info(self, first_name="Alexandr", last_name="Petrov"):
        logger.info("🔹 Filling basic info: %s %s", first_name, last_name)
        self.click(self.PIM_TAB)
        self.click(self.ADD_BUTTON)
        self.send_keys(self.FIRST_NAME, first_name)
        self.send_keys(self.LAST_NAME, last_name)
        employee_id = generate_unique_employee_id()
        username = generate_unique_username()
        self.send_keys_force_clear(self.EMPLOYEE_ID, employee_id)
        self.click(self.ENABLE_LOGIN_TOGGLE)
        self.send_keys(self.USERNAME_FIELD, username)
        self.send_keys(self.PASSWORD_FIELD, "Pass123!")
        self.send_keys(self.CONFIRM_PASSWORD_FIELD, "Pass123!")
        self.upload_profile_picture(self.PROFILE_PICTURE, self.UPLOAD_INPUT_PIC)
        self.click(self.SUBMIT_BUTTON)
        logger.info("✅ Basic employee created: %s / %s", username, employee_id)
        return employee_id, username

    @allure.step("Filling additional employee info")
    def fill_additional_info(self):
        logger.info("🔹 Filling additional fields")
        self.send_keys(self.LICENSE_NUMBER_LABEL, "233821")
        self.send_keys(self.LICENSE_EXP_LABEL, "2030-01-01")
        self.select_dropdown_by_label("Nationality", "Russian", self.DROPDOWN_LISTBOX, self.DROPDOWN_OPTIONS,
                                      fail_if_missing=False)
        self.select_dropdown_by_label("Marital Status", "Single", self.DROPDOWN_LISTBOX, self.DROPDOWN_OPTIONS)
        self.send_keys(self.DATE_OF_BIRTH_LABEL, "2000-01-01")
        self.click(self.MALE_LABEL)
        self.click(self.SUBMIT_BUTTON_TYPE)
        self.click(self.JOB_TAB)
        self.send_keys(self.JOINED_DATE_LABEL, "2022-12-01")
        self.select_dropdown_by_label("Job Title", "QA Engineer", self.DROPDOWN_LISTBOX, self.DROPDOWN_OPTIONS,
                                      fail_if_missing=False)
        self.select_dropdown_by_label("Sub Unit", "Quality Assurance", self.DROPDOWN_LISTBOX, self.DROPDOWN_OPTIONS)
        self.select_dropdown_by_label("Employment Status", "Full-Time Contract", self.DROPDOWN_LISTBOX,
                                      self.DROPDOWN_OPTIONS, fail_if_missing=False)
        self.click(self.SUBMIT_BUTTON)
        logger.info("✅ Additional information saved")

    @allure.step("Finalizing employee creation and verification")
    def finalize_employee_creation(self, employee_id, username):
        save_employee_to_csv(username, employee_id)
        logger.info("🗂 Employee saved to CSV: %s / %s", username, employee_id)
        self.click(self.PIM_TAB)
        self.send_keys_force_clear(self.EMPLOYEE_ID, employee_id)
        self.click(self.SUBMIT_BUTTON)



    @allure.step("Search employee by ID: {employee_id}")
    def search_employee_by_id(self, employee_id):
        logger.info("🔍 Searching employee by ID: %s", employee_id)
        self.click(self.PIM_TAB)
        self.send_keys_force_clear(self.EMPLOYEE_ID, employee_id)
        self.click(self.SUBMIT_BUTTON)
        return  self.find_employee_in_table_by_id(employee_id, self.EMPLOYEE_TABLE, self.EMPLOYEE_ROWS)


