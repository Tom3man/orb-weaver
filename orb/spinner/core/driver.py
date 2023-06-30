import logging
from typing import Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager

from orb.common.design.welcome_page import build_welcome_page
from orb.utils import GetProxies, GetUserAgent
from orb.utils.decorators import retry_on_failure

log = logging.getLogger(__name__)


class OrbDriver:
    """
    This class builds an instance of a Chrome WebDriver utilizing a random proxy and headers (which can be rotated).
    The driver instance can be created using the `get_webdriver` method.
    """

    def __init__(self, headless=None, https: bool = False) -> None:
        """
        Initialize OrbDriver.

        Args:
            headless (bool): Optional. Whether to run the browser in headless mode.
            https (bool): Optional. Whether to use an HTTPS/SSL proxy.
        """
        self.headless = headless
        self.driver_install = None
        self.proxy_dict = None
        self.https = https

    @property
    def random_user_agent(self) -> str:
        """
        Get a random User-Agent string.

        Returns:
            str: A random User-Agent string.
        """
        return GetUserAgent().headers_dict['User-Agent']

    @retry_on_failure(max_retries=3)
    def random_proxy(self, add_https: bool = False) -> Dict[str, str]:
        """
        Get a random proxy.

        Args:
            add_https (bool): Whether to consider an HTTPS/SSL proxy alongside a regular HTTP proxy.

        Returns:
            dict: A dictionary containing the HTTP and (optionally) HTTPS/SSL proxy information.

        Raises:
            RuntimeError: If a working proxy cannot be found.
        """

        proxy_dict = GetProxies().proxy_dict

        if proxy_dict:
            self.proxy = Proxy()
            self.proxy.proxy_type = ProxyType.MANUAL

            # Add HTTP proxy
            self.proxy.http_proxy = proxy_dict['http']

            # Add HTTPS/SSL proxy if enabled
            if add_https:
                self.proxy.ssl_proxy = proxy_dict['https']

            self.proxy.add_to_capabilities(self.capabilities)
            self.proxy_dict = proxy_dict
        else:
            raise RuntimeError("Failed to add a working proxy.")

    def _webdriver_options_init(self):
        """
        Initialize WebDriver options and capabilities.
        """
        self.webdriver_options = Options()
        self.capabilities = webdriver.DesiredCapabilities.CHROME

        self.webdriver_options.add_argument("--disable-javascript")

        if self.headless:
            self.webdriver_options.add_argument("--headless")

        user_agent = self.random_user_agent
        log.info(f"Initializing WebDriver with user-agent: {user_agent}")
        self.webdriver_options.add_argument(f"user-agent={user_agent}")

        self.random_proxy(add_https=self.https)

    def driver_init__(self):
        """
        Initialize WebDriver installation.
        """
        self.driver_install = ChromeDriverManager().install()

    def get_webdriver(self):
        """
        Gets an instance of the Chrome WebDriver.

        Returns:
            selenium.webdriver.Chrome: An instance of the Chrome WebDriver.
        """
        self._webdriver_options_init()

        if not self.driver_install:
            self.driver_init__()

        if not self.driver:
            self.driver = webdriver.Chrome(
                self.driver_install,
                options=self.webdriver_options,
                service=self.service
            )

        # Builds a landing page for the driver to start at
        build_welcome_page(
            driver=self.driver,
            proxy_info=self.proxy_dict,
        )

        return self.driver

    def set_driver(self, driver):
        """
        Set the driver instance. THis is useful for testing.

        Args:
            driver: The WebDriver instance to set.
        """
        self.driver = driver
