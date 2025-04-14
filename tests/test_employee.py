import time

import allure

from pages.employee_page import EmployeePage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from utils.logger import logger

"""def test_employee_login(driver, employee_user):
    logger.info("🚀 Running test: employee_login")
    username, password = employee_user
    login_page = LoginPage(driver)

    login_page.login(username, password)
    employee_page = EmployeePage(driver)
    assert employee_page.is_logged_in()
    logger.info("✅ The test completed successfully!: employee_login")
    """