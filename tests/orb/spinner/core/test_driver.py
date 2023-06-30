import unittest
from unittest.mock import MagicMock

from selenium.webdriver import Chrome
from selenium.webdriver.common.proxy import ProxyType

from orb import REPO_PATH
from orb.spinner.core.driver import OrbDriver


class OrbDriverTestCase(unittest.TestCase):
    """
    Unit tests for the OrbDriver class.
    """

    WELCOME_PAGE_PATH = f"{REPO_PATH}/proxy_info.html"

    def setUp(self):
        """
        Set up the test case by creating mock objects for the driver and proxy.
        """
        self.mock_driver = MagicMock(spec=Chrome)
        self.mock_proxy = MagicMock(spec=ProxyType)
        self.mock_driver.proxy = self.mock_proxy

    def test_get_webdriver(self):
        """
        Test the get_webdriver method of OrbDriver class.
        """
        # Create an instance of OrbDriver
        orb_driver = OrbDriver()

        # Set the mock driver
        orb_driver.set_driver(self.mock_driver)

        # Call the get_webdriver() method
        result = orb_driver.get_webdriver()

        # Assertions
        self.assertEqual(result, self.mock_driver)
        self.mock_driver.get.assert_called_with(f'file://{self.WELCOME_PAGE_PATH}')

        # Check if a proxy is being used correctly
        self.assertTrue(orb_driver.driver.proxy is not None)
        self.assertEqual(orb_driver.driver.proxy, self.mock_proxy)


if __name__ == '__main__':
    unittest.main()
