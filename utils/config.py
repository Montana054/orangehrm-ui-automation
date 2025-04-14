from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

BROWSER_CONFIG = {
    "chrome": (ChromeService, lambda: None, ChromeOptions),
    "firefox": (FirefoxService, lambda: GeckoDriverManager().install(), FirefoxOptions),
    "edge": (EdgeService, lambda: EdgeChromiumDriverManager().install(), EdgeOptions),
}

def get_driver(browser: str = "chrome", headless: bool = False):
    if browser not in BROWSER_CONFIG:
        raise ValueError(f"❌ Unsupported browser: {browser}")

    service_class, driver_path_func, options_class = BROWSER_CONFIG[browser]
    options = options_class()

    if headless:
        if browser == "firefox":
            options.headless = True
        else:
            options.add_argument("--headless=new")

    driver_path = driver_path_func()
    service = service_class() if driver_path is None else service_class(executable_path=driver_path)

    if browser == "chrome":
        return webdriver.Chrome(service=service, options=options)
    elif browser == "firefox":
        return webdriver.Firefox(service=service, options=options)
    elif browser == "edge":
        return webdriver.Edge(service=service, options=options)
