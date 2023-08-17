"""Gets the browser's given the user's input"""
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Webdriver managers
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from tiktok_uploader import config, logger
from tiktok_uploader.utils import green

# Added
from seleniumwire import webdriver
from proxy import get_proxy
from dotenv import load_dotenv
from const import *

load_dotenv()


def get_browser(name: str = 'chrome', options=None, *args, **kwargs) -> webdriver:
    """
    Gets a browser based on the name with the ability to pass in additional arguments
    """

    # get the web driver for the browser
    driver_to_use = get_driver(name=name, *args, **kwargs)

    # gets the options for the browser

    options, seleniumwireOptions = options or get_default_options(
        name=name, *args, **kwargs)

    # combines them together into a completed driver
    service = get_service(name=name)
    if service:
        driver = driver_to_use(
            service=service, options=options)
    else:
        driver = driver_to_use(
            options=options)

    driver.implicitly_wait(config['implicit_wait'])
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    logger.debug(green('Driver with proxy created correctly'))

    return driver


def get_driver(name: str = 'chrome', *args, **kwargs) -> webdriver:
    """
    Gets the web driver function for the browser
    """
    if _clean_name(name) in drivers:
        return drivers[name]

    raise UnsupportedBrowserException()


def get_service(name: str = 'chrome'):
    """
    Gets a service to install the browser driver per webdriver-manager docs

    https://pypi.org/project/webdriver-manager/
    """
    if _clean_name(name) in services:
        return services[name]()

    return None  # Safari doesn't need a service


def get_default_options(name: str, *args, **kwargs):
    """
    Gets the default options for each browser to help remain undetected
    """
    name = _clean_name(name)

    if name in defaults:
        return defaults[name](*args, **kwargs)

    raise UnsupportedBrowserException()


def chrome_defaults(*args, headless: bool = False, **kwargs) -> ChromeOptions:
    """
    Creates Chrome with Options
    """

    options = ChromeOptions()

    # regular
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--profile-directory=Default')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument(f"user-agent={RANDOM_USER_AGENT}")
    options.add_argument('--start-maximized')

    # experimental
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    proxyUrl = get_proxy()
    seleniumwireOptions = {
        "proxy": {
            "http": proxyUrl,
            "https": proxyUrl,
            "no_proxy": ""
        }
    }

    # headless
    if headless:
        options.add_argument('--headless=new')

    return options, seleniumwireOptions

# Misc


class UnsupportedBrowserException(Exception):
    """
    Browser is not supported by the library

    Supported browsers are:
        - Chrome
        - Firefox
        - Safari
        - Edge
    """

    def __init__(self, message=None):
        super().__init__(message or self.__doc__)


def _clean_name(name: str) -> str:
    """
    Cleans the name of the browser to make it easier to use
    """
    return name.strip().lower()


drivers = {
    'chrome': webdriver.Chrome,
}

defaults = {
    'chrome': chrome_defaults
}


services = {
    'chrome': lambda: ChromeService(ChromeDriverManager().install()),
}
