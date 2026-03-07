import logging
from typing import Dict

import requests

from orb.net import request_get_with_retry

log = logging.getLogger(__name__)
__test__ = False


def test_proxy(proxies: Dict[str, str]) -> bool:
    """
    Test the functionality of a proxy by making a request to a sample URL.

    Args:
        proxies (Dict[str, str]): Dictionary containing HTTP and HTTPS proxies.

    Returns:
        bool: True if the proxy is working, False otherwise.
    """
    try:
        url = 'http://www.example.com'
        response = request_get_with_retry(
            url,
            proxies=proxies,
            timeout=5,
            max_retries=2,
            backoff_seconds=0.25,
        )
        if response.status_code == 200:
            log.info(f"{proxies['https']} Proxy is working!")
            return True
        else:
            log.error(f"{proxies['https']} Proxy is NOT working!")
            return False
    except requests.exceptions.RequestException:
        log.error("Unable to connect to the proxy.")
        return False
