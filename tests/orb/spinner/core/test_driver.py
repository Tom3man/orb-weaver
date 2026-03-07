import unittest
from unittest.mock import MagicMock, patch

from orb.spinner.core.driver import OrbDriver


class OrbDriverTestCase(unittest.TestCase):
    """
    Unit tests for the OrbDriver class.
    """
    @patch("orb.spinner.core.driver.Service")
    @patch("orb.spinner.core.driver.webdriver.Chrome")
    @patch("orb.spinner.core.driver.ChromeDriverManager.install")
    def test_get_webdriver(self, mock_install, mock_chrome, mock_service):
        """
        Test the get_webdriver method without making network calls.
        """
        mock_install.return_value = "/tmp/chromedriver"
        mock_service.return_value = MagicMock()
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        orb_driver = OrbDriver(use_pia=False)
        result = orb_driver.get_webdriver()

        self.assertEqual(result, mock_driver)
        mock_chrome.assert_called_once()
        mock_driver.get.assert_not_called()

    @patch("orb.spinner.core.driver.Service")
    @patch("orb.spinner.core.driver.webdriver.Chrome")
    @patch("orb.spinner.core.driver.ChromeDriverManager.install")
    def test_get_webdriver_with_url(self, mock_install, mock_chrome, mock_service):
        mock_install.return_value = "/tmp/chromedriver"
        mock_service.return_value = MagicMock()
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        orb_driver = OrbDriver(use_pia=False)
        result = orb_driver.get_webdriver(url="https://example.com")

        self.assertEqual(result, mock_driver)
        mock_driver.get.assert_called_once_with(url="https://example.com")


if __name__ == '__main__':
    unittest.main()
