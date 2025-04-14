import allure
from pages.login_page import LoginPage
from pages.main_page import MainPage
from utils.logger import logger

@allure.story("Login")
@allure.title("Valid login test as Admin")
@allure.step("Test: Login as Admin")
def test_login_admin(authenticated_driver):
    logger.info("🚀 Running test: test_login_admin")
    main_page = MainPage(authenticated_driver)
    assert main_page.is_employee_logged_in(), "❌ ERROR: Admin login failed — label not visible"
    logger.info("✅ Test passed: login as Admin")

@allure.story("Login")
@allure.title("Invalid login test with wrong password")
@allure.step("Test: Login with invalid password")
def test_login_invalid_password(driver):
    logger.info("🚀 Running test: login with invalid password")
    login_page = LoginPage(driver)
    login_page.login("Admin", "admin123!")
    error_message = login_page.get_error_message()
    logger.info(f"🔹 Retrieved error message: {error_message}")
    assert error_message is not None, "❌ ERROR: Error message element was not found"
    assert "Invalid credentials" in error_message, f"❌ ERROR: Expected 'Invalid credentials', but got: '{error_message}'"
    logger.info("✅ The test completed successfully!: test_login_invalid_password")
