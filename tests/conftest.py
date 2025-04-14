import os
from datetime import datetime

import allure
import pytest
from pages.login_page import LoginPage
from pages.main_page import MainPage
from utils.logger import logger


from utils.config import get_driver

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )

@pytest.fixture()
def driver(request):
    browser = request.config.getoption("browser")
    headless = request.config.getoption("headless")

    logger.debug(f"🧪 Launching {browser} (headless={headless})")
    driver = get_driver(browser, headless=headless)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()
    yield driver
    logger.debug(f"🔴 Quitting {browser} driver")
    driver.quit()

"""@pytest.fixture()
def driver():
    logger.debug("🟢 Starting the Chrome driver")
    driver = webdriver.Chrome()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()
    yield driver
    logger.debug("🔴 Closing the Chrome driver")
    driver.quit()"""

@pytest.fixture
def employee_user(authenticated_driver):
    page = MainPage(authenticated_driver)
    username = page.create_employee_user()
    return username, "Pass123!"

@allure.step("PRECONDITION: Login as Admin")
@pytest.fixture()
def authenticated_driver(driver):
    logger.info("🔹 PRECONDITION - Let's log into the system")
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page = LoginPage(driver)
    main_page = MainPage(driver)
    try:
        login_page.login("Admin", "admin123")
        if main_page.is_employee_logged_in():
            logger.info("✅ PRECONDITION - Login successful")
        else:
            logger.error("🚨 PRECONDITION FAILED: Admin login failed, no error detected")
            pytest.fail("PRECONDITION FAILED: Login was not successful")
    except Exception as e:
        logger.error(f"🚨 PRECONDITION FAILED: Login error: {e}")
        pytest.fail(f"PRECONDITION FAILED: {e}")

    yield driver

    test_name = os.getenv('PYTEST_CURRENT_TEST', '')
    if "test_logout" in test_name:
        logger.info("🔹 POSTCONDITION SKIPPED for test_logout")
        return
    with allure.step("POSTCONDITION: Logout from Admin"):
        try:
            main_page = MainPage(driver)
            main_page.logout()
            logger.info("🔸 POSTCONDITION: Successfully logged out")
        except Exception as e:
            logger.warning(f"⚠️ POSTCONDITION FAILED: Logout skipped or failed: {e}")

# --- Screenshot on test failure ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshots")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed and "driver" in item.funcargs:
        driver = item.funcargs["driver"]
        test_name = item.name
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")
        with open(screenshot_path, "rb") as f:
            allure.attach(f.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
