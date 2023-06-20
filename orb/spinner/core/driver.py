import logging
import random
from typing import Dict

from orb.spinner.utils.spoofing import DriverSpoofing
from orb.utils import GetProxies, GetUserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

log = logging.getLogger(__name__)


class OrbDriver:

    """
    This class builds an instance of a chrome driver utilising a random proxy and headers (which can be rotated).
    The driver instance can be created using the get_webdriver method.
    """

    def __init__(self, *args, **kwargs):
        self.driver_spoof = DriverSpoofing()

        if kwargs.get('headless'):
            self.headless = kwargs['headless']
        else:
            self.headless = None

        self.driver_install = None

    @property
    def random_user_agent(self) -> 'GetUserAgent':
        return GetUserAgent().headers_dict['User-Agent']

    @property
    def random_proxy(self) -> 'GetProxies':
        return GetProxies().proxy_dict['https']

    def _webdriver_options_init(self):

        # Initialise webdriver options
        self.webdriver_options = Options()

        # Default webdriver options
        # Disable javascript
        self.webdriver_options.add_argument("--disable-javascript")

        # Set to headless if applicable
        if self.headless:
            self.webdriver_options.add_argument("--headless")

        # Set the user agent string
        user_agent = self.random_user_agent
        log.info(f"Initialising webdriver with user-agent: {user_agent} ")
        self.webdriver_options.add_argument(f"user-agent={user_agent}")

        # Set the proxy string
        proxy = self.random_proxy
        log.info(f"Initialising webdriver with proxy: {proxy} ")
        self.webdriver_options.add_argument(f'--proxy-server={proxy}')

    def change_driver_viewport(self):

        self.driver_spoof.change_viewport_size(
            driver=self.driver
        )

    def driver_init__(self):

        # Always install the latest web driver
        self.driver_install = ChromeDriverManager().install()

    def get_webdriver(self) -> webdriver.Chrome:

        # Initialise webdriver options
        self._webdriver_options_init()

        # Always install the latest web driver
        # Initialize the webdriver with the options
        if not self.driver_install:
            self.driver_init__()
            self.driver = webdriver.Chrome(self.driver_install, options=self.webdriver_options)

        self.driver = webdriver.Chrome(options=self.webdriver_options)

        return self.driver

    def get_url(self, driver: webdriver.Chrome = None):
        if not driver:
            self.driver = self.get_webdriver()
        else:
            self.driver = driver
