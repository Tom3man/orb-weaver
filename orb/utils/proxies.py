import logging
from datetime import datetime
from typing import Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup
from orb.utils.utils import timeout

log = logging.getLogger(__name__)


def test_proxy(proxies: Dict[str, str]):
    """
    A testing function that can be used to test if a proxy if working.
    Args:
        proxies: Dictionary containing http and https proxies for testing
    Returns:
        Bool statement if proxy is working.
    """
    try:
        # Define the URL you want to access through the proxy
        url = 'http://www.example.com'

        # Make a request using the proxy
        response = requests.get(url, proxies=proxies, timeout=5)

        # Check the response status code
        if response.status_code == 200:
            log.info(f"{proxies['https']} Proxy is working!")
        else:
            log.error(f"{proxies['https']} Proxy is NOT working!")
    except requests.exceptions.RequestException:
        log.error("Unable to connect to the proxy.")


class GetProxies:
    """
    A class for retrieving and working with proxy information.
    """

    PROXY_SITE = "https://free-proxy-list.net/"

    def __init__(self) -> None:
        """
        Initializes the GetProxies object.
        Sets the current date and time.
        """
        todays_datetime = datetime.now()
        self.date_now = todays_datetime.strftime("%Y-%m-%d")
        self.time_now = todays_datetime.strftime("%H:%M")

    @timeout(seconds=10, error_message="request url method")
    def request_proxies(self) -> requests:
        """
        Sends a request to the proxy URL and returns the request object.
        """
        return requests.get(self.PROXY_SITE)

    def parse_requests(self) -> BeautifulSoup:
        """
        Parses the returned request from request_proxies and returns a BeautifulSoup object.
        """
        return BeautifulSoup(self.request_proxies().content, 'html.parser')

    def extract_table_html(self) -> BeautifulSoup:
        """
        Returns the raw HTML of the table containing the proxy information.
        """
        return self.parse_requests().find('table')

    def return_proxy_table(self, https_only: bool = True) -> pd.DataFrame:
        """
        Iterates through the HTML table to build a pandas DataFrame of proxies.
        If https_only is True, returns only proxies with HTTPS support.
        """
        df = pd.DataFrame()
        headers = None
        for tr in self.extract_table_html().find_all('tr'):
            if not headers:
                headers = [
                    td.text.upper().replace(" ", "_") for td in tr.find_all(
                        ['th', 'td']
                    )
                ]
                df = pd.DataFrame(columns=headers)
                continue

            df.loc[len(df)] = [
                td.text for td in tr.find_all(['th', 'td'])]

        if https_only:
            return df[df['HTTPS'] == 'yes']
        return df

    @property
    def proxy_dict(self) -> Dict[str, str]:
        """
        Returns a dictionary of HTTP and HTTPS proxy values.
        The dictionary can be used for further web scraping.
        """
        # Build proxy pandas DataFrame
        proxy_table = self.return_proxy_table(https_only=True)

        # Select random row from DataFrame
        proxy_row = proxy_table.sample(1)

        ip_address = proxy_row['IP_ADDRESS'].values[0]
        port = proxy_row['PORT'].values[0]

        proxies = {
            "http": f"{ip_address}:{port}",
            "https": f"{ip_address}:{port}",
        }

        if test_proxy(proxies=proxies):
            return proxies
        self.proxy_dict()
