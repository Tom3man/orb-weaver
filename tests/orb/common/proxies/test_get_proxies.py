import logging
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag

from orb.common.proxies.get_proxies import GetProxies

log = logging.getLogger(__name__)


class GetProxiesTests(unittest.TestCase):

    def setUp(self):
        self.getproxies = GetProxies()

    def test_request_proxies(self):
        with patch.object(requests, 'get') as mock_get:
            response = MagicMock()
            mock_get.return_value = response
            self.assertEqual(self.getproxies.request_proxies(), response)
            mock_get.assert_called_once_with(GetProxies.PROXY_SITE)

    def test_parse_requests(self):
        with patch.object(self.getproxies, 'request_proxies') as mock_request:
            response = MagicMock()
            response.content = b'<html><body><table></table></body></html>'
            mock_request.return_value = response
            parsed_html = self.getproxies.parse_requests()
            self.assertIsInstance(parsed_html, BeautifulSoup)

    def test_extract_table_html(self):
        with patch.object(self.getproxies, 'parse_requests') as mock_parse:
            soup = BeautifulSoup('<table></table>', 'html.parser')
            mock_parse.return_value = soup
            table_html = self.getproxies.extract_table_html()
            self.assertIsInstance(table_html, Tag)
            self.assertEqual(str(table_html), '<table></table>')

    def test_return_proxy_table(self):
        with patch.object(self.getproxies, 'extract_table_html') as mock_extract:
            soup = BeautifulSoup('<table><thead><tr><th>IP</th><th>Port</th></tr></thead><tbody><tr><td>1.2.3.4</td><td>8080</td></tr><tr><td>5.6.7.8</td><td>8888</td></tr></tbody></table>', 'html.parser')
            mock_extract.return_value = soup
            proxy_table = self.getproxies.return_proxy_table(https_only=False)
            print(proxy_table)  # Added print statement
            print(proxy_table.shape)  # Added print statement
            self.assertIsInstance(proxy_table, pd.DataFrame)
            self.assertEqual(proxy_table.shape, (2, 2))

    def test_build_proxy_dict(self):
        with patch.object(self.getproxies, 'return_proxy_table') as mock_return:
            df = pd.DataFrame({'IP_ADDRESS': ['1.2.3.4'], 'PORT': ['8080'], 'HTTPS': ['yes']})
            mock_return.return_value = df
            self.getproxies.build_proxy_dict()
            self.assertEqual(self.getproxies.proxies, {'http': '1.2.3.4:8080', 'https': '1.2.3.4:8080'})


if __name__ == '__main__':
    unittest.main()
