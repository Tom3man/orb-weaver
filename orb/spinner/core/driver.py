import logging
from typing import Dict, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# from orb.common.design.welcome_page import build_welcome_page
from orb.common.vpn import PiaVpn
from orb.utils import GetUserAgent

log = logging.getLogger(__name__)


class OrbDriver:
    """
    OrbDriver builds an instance of a Chrome WebDriver with optional features like headless mode,
    HTTPS/SSL proxy, and custom user-agent.
    """

    def __init__(self, webdriver_path: Optional[str] = None, use_pia: Optional[bool] = True) -> None:
        """
        Initialize OrbDriver with default options.
        """
        self.driver = None
        self.webdriver_path = webdriver_path
        self.webdriver_options = Options()

        # Placeholder for PiaVpn instance
        if use_pia:
            self.pia = PiaVpn()
        else:
            self.pia = None

    def _webdriver_init__(self) -> None:
        """
        Initialise WebDriver installation and options.
        """
        # Download latest webdriver
        if not self.webdriver_path:
            self.webdriver_path = ChromeDriverManager().install()
        self.webdriver_service = Service(executable_path=self.webdriver_path)

        # Common options for WebDriver
        self.webdriver_options.add_argument("--disable-javascript")
        self.webdriver_options.add_argument('--no-sandbox')
        self.webdriver_options.add_argument('--disable-dev-shm-usage')
        self.webdriver_options.add_argument('--blink-settings=imagesEnabled=false')
        self.webdriver_options.add_argument('--disable-extensions')
        self.webdriver_options.add_argument('--disable-blink-features=AutomationControlled')
        self.webdriver_options.add_argument('--disable-gpu')
        self.webdriver_options.add_argument('--window-size=1920x1080')
        self.webdriver_options.add_argument('--log-level=3')
        self.webdriver_options.add_argument('--disable-web-security')
        self.webdriver_options.add_argument(f"user-agent={self.set_user_agent()}")
        self.capabilities = webdriver.DesiredCapabilities.CHROME

    def change_ip_address(self) -> None:
        """
        Change IP address using PIA VPN.
        """
        if self.pia.vpn_status() != 'Connected':
            self.pia.connect()
        else:
            self.pia.set_region(region='random')

    def set_headless(self) -> 'OrbDriver':
        """
        Enable headless mode for the WebDriver.

        Returns:
            OrbDriver: The OrbDriver instance for method chaining.
        """
        self.webdriver_options.add_argument("--headless")
        return self

    def set_user_agent(self) -> Dict[str, str]:
        """
        Set a random user-agent for the WebDriver.

        Returns:
            OrbDriver: The OrbDriver instance for method chaining.
        """
        user_agent = GetUserAgent().headers_dict['User-Agent']
        log.info(f"Initialising WebDriver with user-agent: {user_agent}")
        return user_agent

    def get_webdriver(self, url: Optional[str] = None) -> webdriver.Chrome:
        """
        Get an instance of the Chrome WebDriver.

        Returns:
            selenium.webdriver.Chrome: An instance of the Chrome WebDriver.
        """
        self._webdriver_init__()

        self.driver = webdriver.Chrome(
            service=self.webdriver_service, options=self.webdriver_options)

        if url:
            self.driver.get(url=url)
            return self.driver

        # # Builds a landing page for the driver to start at
        # build_welcome_page(driver=self.driver)

        return self.driver

    def refresh_driver(self) -> webdriver.Chrome:
        """
        Refreshes the given WebDriver instance by closing the current session and creating a new one.

        Args:
            driver (webdriver.Chrome): The current WebDriver instance to be refreshed.

        Returns:
            webdriver.Chrome: A new WebDriver instance pointing to the same URL as the closed session.
        """
        # Store the current URL
        current_url = self.driver.current_url

        # Close the current WebDriver session
        self.driver.quit()

        # if current_url.split('.')[-1] == 'html':
        #     self.driver = self.get_webdriver()
        #     build_welcome_page(driver=self.driver)

        # Initialise a new WebDriver session with the same URL
        self.driver = self.get_webdriver(url=current_url)

        return self.driver

    def set_driver(self, driver: webdriver.Chrome) -> None:
        """
        Set the WebDriver instance. Useful for testing.

        Args:
            driver (webdriver.Chrome): The WebDriver instance to set.
        """
        self.driver = driver
