import unittest
from unittest.mock import MagicMock, patch

import requests
from orb.utils.proxies import GetProxies


class TestGetProxies(unittest.TestCase):
    def setUp(self):
        self.get_proxies = GetProxies()

    def test_init(self):
        self.assertIsInstance(self.get_proxies.date_now, str)
        self.assertIsInstance(self.get_proxies.time_now, str)

    @patch.object(requests, 'get')
    def test_request_proxies(self, mock_get):
        mock_response = MagicMock()
        mock_get.return_value = mock_response

        result = self.get_proxies.request_proxies()

        mock_get.assert_called_once_with(GetProxies.PROXY_SITE)
        self.assertEqual(result, mock_response)

    def test_parse_requests(self):
        mock_response = MagicMock(
            content='<html><body>Mock HTML</body></html>')
        mock_beautiful_soup = MagicMock(return_value=mock_response)
        self.get_proxies.request_proxies = MagicMock(
            return_value=mock_response)

        with patch(
            'orb.utils.proxies.BeautifulSoup',
            side_effect=mock_beautiful_soup
        ):
            result = self.get_proxies.parse_requests()

        self.assertEqual(result, mock_response)

    def test_extract_table_html(self):
        mock_table_html = MagicMock()
        mock_find = MagicMock(return_value=mock_table_html)
        self.get_proxies.parse_requests = MagicMock(
            return_value=MagicMock(find=mock_find))

        result = self.get_proxies.extract_table_html()

        mock_find.assert_called_once_with('table')
        self.assertEqual(result, mock_table_html)


if __name__ == '__main__':
    unittest.main()
