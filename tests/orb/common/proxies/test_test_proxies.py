import unittest
from unittest.mock import MagicMock, patch
from typing import Dict
import requests

from orb.common.proxies.test_proxies import test_proxy


class TestProxy(unittest.TestCase):
    """
    Test case for the test_proxy function.

    The TestProxy class contains test methods to verify the behavior of the test_proxy function
    in different scenarios.
    """

    TEST_URL: Dict[str, str] = {
        'HTTP': 'http://proxy.example.com',
        'HTTPS': 'https://proxy.example.com'
    }

    @patch('requests.get')
    @patch('logging.Logger.info')
    def test_working_proxy(self, mock_info, mock_get):
        """
        Test the behavior of the test_proxy function for a working proxy.

        This test method mocks the requests.get function to return a successful response (status_code = 200)
        and verifies that the test_proxy function returns True. It also checks if the expected log message
        is logged using the info method of the logging.Logger class.

        Args:
            mock_info (MagicMock): Mock object for the info method of the logging.Logger class.
            mock_get (MagicMock): Mock object for the requests.get function.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        proxies = {'http': self.TEST_URL['HTTP'], 'https': self.TEST_URL['HTTPS']}
        result = test_proxy(proxies)
        self.assertTrue(result)
        mock_info.assert_called_with("https://proxy.example.com Proxy is working!")

    @patch('requests.get')
    @patch('logging.Logger.error')
    def test_non_working_proxy(self, mock_error, mock_get):
        """
        Test the behavior of the test_proxy function for a non-working proxy.

        This test method mocks the requests.get function to return a failed response (status_code = 500)
        and verifies that the test_proxy function returns False. It also checks if the expected log message
        is logged using the error method of the logging.Logger class.

        Args:
            mock_error (MagicMock): Mock object for the error method of the logging.Logger class.
            mock_get (MagicMock): Mock object for the requests.get function.
        """
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        proxies = {'http': self.TEST_URL['HTTP'], 'https': self.TEST_URL['HTTPS']}
        result = test_proxy(proxies)
        self.assertFalse(result)
        mock_error.assert_called_with("https://proxy.example.com Proxy is NOT working!")

    @patch('requests.get')
    @patch('logging.Logger.error')
    def test_connection_error(self, mock_error, mock_get):
        """
        Test the behavior of the test_proxy function for a connection error.

        This test method mocks the requests.get function to raise a requests.exceptions.RequestException
        and verifies that the test_proxy function returns False. It also checks if the expected log message
        is logged using the error method of the logging.Logger class.

        Args:
            mock_error (MagicMock): Mock object for the error method of the logging.Logger class.
            mock_get (MagicMock): Mock object for the requests.get function.
        """
        mock_get.side_effect = requests.exceptions.RequestException()
        proxies = {'http': self.TEST_URL['HTTP'], 'https': self.TEST_URL['HTTPS']}
        result = test_proxy(proxies)
        self.assertFalse(result)
        mock_error.assert_called_with("Unable to connect to the proxy.")


if __name__ == '__main__':
    unittest.main()
