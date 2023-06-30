import logging
from datetime import datetime
from typing import Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag

from orb.common.proxies.test_proxies import test_proxy

log = logging.getLogger(__name__)


class GetProxies:
    """
    A class for retrieving and working with proxy information.
    """

    PROXY_SITE = "https://free-proxy-list.net/"

    def __init__(self) -> None:
        """
        Initializes the GetProxies object and sets the current date and time.
        """
        todays_datetime = datetime.now()
        self.date_now = todays_datetime.strftime("%Y-%m-%d")
        self.time_now = todays_datetime.strftime("%H:%M")

    def request_proxies(self) -> requests.Response:
        """
        Sends a request to the proxy URL and returns the response object.

        Returns:
            requests.Response: The response object from the request.
        """
        return requests.get(self.PROXY_SITE)

    def parse_requests(self) -> BeautifulSoup:
        """
        Parses the returned request from request_proxies and returns a BeautifulSoup object.

        Returns:
            BeautifulSoup: The BeautifulSoup object representing the parsed HTML.
        """
        return BeautifulSoup(self.request_proxies().content, 'html.parser')

    def extract_table_html(self) -> Tag:
        """
        Extracts the raw HTML of the table containing the proxy information.

        Returns:
            BeautifulSoup: The BeautifulSoup object representing the extracted HTML.
        """
        return self.parse_requests().find('table')

    def return_proxy_table(self, https_only: bool = True) -> pd.DataFrame:
        """
        Iterates through the HTML table to build a pandas DataFrame of proxies.

        Args:
            https_only (bool, optional): Whether to return only proxies with HTTPS support.

        Returns:
            pd.DataFrame: The pandas DataFrame containing the proxy information.
        """
        df = pd.DataFrame()
        headers = None
        for tr in self.extract_table_html().find_all('tr'):
            if not headers:
                headers = [
                    td.text.upper().replace(" ", "_") for td in tr.find_all(['th', 'td'])
                ]
                df = pd.DataFrame(columns=headers)
                continue

            df.loc[len(df)] = [td.text for td in tr.find_all(['th', 'td'])]

        if https_only:
            return df[df['HTTPS'] == 'yes']
        return df

    def build_proxy_dict(self) -> None:
        """
        Builds a dictionary of HTTP and HTTPS proxy values from the proxy table DataFrame.
        """
        proxy_table = self.return_proxy_table(https_only=True)
        proxy_row = proxy_table.sample(1)
        ip_address = proxy_row['IP_ADDRESS'].values[0]
        port = proxy_row['PORT'].values[0]

        self.proxies = {
            "http": f"{ip_address}:{port}",
            "https": f"{ip_address}:{port}",
        }

    @property
    def proxy_dict(self) -> Dict[str, str]:
        """
        Property that returns the proxy dictionary.

        Returns:
            Dict[str, str]: The dictionary containing HTTP and HTTPS proxy values.

        Raises:
            RuntimeError: If a working proxy cannot be found after maximum retries.
        """

        self.build_proxy_dict()
        if test_proxy(proxies=self.proxies):
            return self.proxies
        raise RuntimeError("Failed to find a working proxy.")
