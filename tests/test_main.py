import allure
import pytest

from pages.employee_page import EmployeePage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from tests.conftest import authenticated_driver
from utils.data_helper import read_last_user_from_csv, CSV_PATH, save_employee_to_csv
from utils.logger import logger

@allure.story("Session Management")
@allure.title("Logout from the system as Admin")
@allure.step("Logout from the system")
def test_logout(authenticated_driver):
    logger.info("🚀 Running test: test_logout")
    main_page = MainPage(authenticated_driver)
    main_page.logout()
    assert main_page.is_logged_out(), \
        "❌ Logout failed!"
    logger.info("✅ Test passed: test_logout")


# full flow

@allure.story("Employee Management")
@allure.title("Add new employee and verify creation")
@allure.step("Test: Add employee")
def test_add_employee(authenticated_driver):
    logger.info("🚀 Running test: add_employee")
    main_page = MainPage(authenticated_driver)
    employee_id, username = main_page.fill_basic_info()
    assert main_page.is_message_displayed(main_page.SUCCESS_MESSAGE, "Successfully Saved"), \
        "❌ ERROR: Success message 'Saved' not shown!"
    main_page.fill_additional_info()
    assert main_page.is_message_displayed(main_page.SUCCESS_MESSAGE, "Successfully Updated"), \
        "❌ ERROR: Success message 'Updated' not shown!"
    main_page.finalize_employee_creation(employee_id, username)
    assert main_page.search_employee_by_id(employee_id), \
        f"❌ ERROR: Employee with ID {employee_id} not found in table!"
    logger.info("✅ Test passed: test_add_employee")

@allure.story("Employee Management")
@allure.title("Create user for employee (light flow)")
@allure.step("Test: Create user for employee")
def test_create_employee_user(authenticated_driver):
    logger.info("🚀 Running test: create_employee_user")
    main_page = MainPage(authenticated_driver)
    employee_id, username = main_page.fill_basic_info()
    assert main_page.is_message_displayed(main_page.SUCCESS_MESSAGE, "Successfully Saved"), \
        "❌ ERROR: Success message 'Saved' not shown!"
    save_employee_to_csv(username, employee_id)
    logger.info("✅ Test passed: test_create_employee_user")


@allure.story("Employee Verification")
@allure.title("Verify if created employees from CSV exist in the table")
@allure.step("Test: Check if employees from CSV are present in the table")
def test_employees_from_csv_present_in_table(authenticated_driver):
    username, employee_id = read_last_user_from_csv()[0]
    logger.info(f"🚀 Checking employee from CSV: {username} / {employee_id}")
    main_page = MainPage(authenticated_driver)
    is_found = main_page.search_employee_by_id(employee_id)
    assert is_found, f"❌ Employee with ID {employee_id} not found in the table!"
    logger.info("✅ Test passed: test_employees_from_csv_present_in_table")

@allure.story("Employee Login")
@allure.title("Full E2E login flow for new employee")
@allure.step("Test: Employee login E2E")
def test_employee_login(driver):
    logger.info("🚀 Running test: employee_login full flow")
    login_page = LoginPage(driver)
    login_page.login("Admin", "admin123")
    main_page = MainPage(driver)
    employee_id, username = main_page.fill_basic_info()
    assert main_page.is_message_displayed(main_page.SUCCESS_MESSAGE, "Successfully Saved"), \
        "❌ ERROR: Success message 'Saved' not shown!"
    main_page.fill_additional_info()
    assert main_page.is_message_displayed(main_page.SUCCESS_MESSAGE, "Successfully Updated"), \
        "❌ ERROR: Success message 'Updated' not shown!"
    main_page.finalize_employee_creation(employee_id, username)
    main_page.logout()
    login_page = LoginPage(driver)
    login_page.login(username, "Pass123!")
    employee_page = EmployeePage(driver)
    expected_name = "Alexandr Petrov"
    assert employee_page.is_employee_logged_in(expected_name), f"❌ Expected user '{expected_name}' is not logged in"
    employee_page.logout_employee()
    logger.info("✅ The test completed successfully!: employee_login")