import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from orb.common.design.welcome_page import build_welcome_page
from orb.common.vpn import PiaVpn
from orb.utils import GetUserAgent

log = logging.getLogger(__name__)


class OrbDriver:
    """
    OrbDriver builds an instance of a Chrome WebDriver with optional features like headless mode,
    HTTPS/SSL proxy, and custom user-agent.
    """

    def __init__(self) -> None:
        """
        Initialize OrbDriver with default options.
        """
        self.driver = None
        self.webdriver_options = Options()

        # Placeholder for PiaVpn instance
        self.pia = PiaVpn()

    def _webdriver_init__(self) -> None:
        """
        Initialize WebDriver installation and options.
        """
        # Download latest webdriver
        self.webdriver_path = ChromeDriverManager().install()
        self.webdriver_service = Service(executable_path=self.webdriver_path)

        # Common options for WebDriver
        self.webdriver_options.add_argument("--disable-javascript")
        self.webdriver_options.add_argument('--no-sandbox')
        self.webdriver_options.add_argument('--disable-dev-shm-usage')

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
        return self  # Return instance for method chaining

    def set_user_agent(self) -> 'OrbDriver':
        """
        Set a random user-agent for the WebDriver.

        Returns:
            OrbDriver: The OrbDriver instance for method chaining.
        """
        user_agent = GetUserAgent().headers_dict['User-Agent']
        log.info(f"Initializing WebDriver with user-agent: {user_agent}")
        self.webdriver_options.add_argument(f"user-agent={user_agent}")
        return self  # Return instance for method chaining

    def get_webdriver(self) -> webdriver.Chrome:
        """
        Get an instance of the Chrome WebDriver.

        Returns:
            selenium.webdriver.Chrome: An instance of the Chrome WebDriver.
        """
        self._webdriver_init__()

        self.driver = webdriver.Chrome(
            service=self.webdriver_service, options=self.webdriver_options)

        # Builds a landing page for the driver to start at
        build_welcome_page(driver=self.driver)

        return self.driver

    def set_driver(self, driver: webdriver.Chrome) -> None:
        """
        Set the WebDriver instance. Useful for testing.

        Args:
            driver (webdriver.Chrome): The WebDriver instance to set.
        """
        self.driver = driver
