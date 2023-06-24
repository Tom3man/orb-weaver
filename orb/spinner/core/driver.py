import logging
from typing import Dict

from orb.spinner.utils import build_welcome_page
from orb.utils import GetProxies, GetUserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

log = logging.getLogger(__name__)


class OrbDriver:
    """
    This class builds an instance of a Chrome WebDriver utilizing a random proxy and headers (which can be rotated).
    The driver instance can be created using the `get_webdriver` method.
    """

    def __init__(self, headless=None) -> None:
        """
        Initialize OrbDriver.

        Args:
            headless (bool): Optional. Whether to run the browser in headless mode.
        """
        self.headless = headless
        self.driver_install = None
        self.proxy_dict = None

    @property
    def random_user_agent(self) -> str:
        """
        Get a random User-Agent string.

        Returns:
            str: A random User-Agent string.
        """
        return GetUserAgent().headers_dict['User-Agent']

    @property
    def random_proxy(self) -> Dict[str, str]:
        """
        Get a random proxy.

        Returns:
            str: A random proxy.

        Raises:
            RuntimeError: If a working proxy cannot be found.
        """
        self.proxy_dict = GetProxies().proxy_dict
        if self.proxy_dict:
            return self.proxy_dict['https']
        raise RuntimeError("Failed to find a working proxy.")

    def _webdriver_options_init(self):
        """
        Initialize WebDriver options.
        """
        self.webdriver_options = Options()
        self.webdriver_options.add_argument("--disable-javascript")

        if self.headless:
            self.webdriver_options.add_argument("--headless")

        user_agent = self.random_user_agent
        log.info(f"Initializing WebDriver with user-agent: {user_agent}")
        self.webdriver_options.add_argument(f"user-agent={user_agent}")

        proxy = self.random_proxy
        log.info(f"Initializing WebDriver with proxy: {proxy}")
        self.webdriver_options.add_argument(f'--proxy-server={proxy}')

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
            self.driver = webdriver.Chrome(
                self.driver_install, options=self.webdriver_options)

        self.driver = webdriver.Chrome(options=self.webdriver_options)

        # Builds a landing page for the driver to start at
        build_welcome_page(
            driver=self.driver,
            proxy_info=self.proxy_dict,
        )

        return self.driver
