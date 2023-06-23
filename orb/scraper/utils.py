"""
This script provides several methods for spoofing requests.
"""

import logging

import requests
from orb.utils.user_agents import GetUserAgent
from orb.utils.proxies import GetProxies

log = logging.getLogger(__name__)


def spoof_request(
    url: str,
    use_proxies: bool = True,
    use_user_agent: bool = True
) -> requests.Response:
    """
    Send a request to a URL with a spoofed user agent and optional proxies.

    Args:
        url (str): The URL to send the request to.
        use_proxies (bool, optional): Whether to use proxies. Defaults to True.
        use_user_agent (bool, optional): Whether to use a random user agent. Defaults to True.

    Returns:
        requests.Response: The response object of the request.
    """

    headers = None
    proxies = None

    # Get a random user agent
    if use_user_agent:
        headers = GetUserAgent().headers_dict

    # Get a random proxy
    if use_proxies:
        proxies = GetProxies().proxy_dict
        log.info(f"Using proxy with HTTPS: {proxies['HTTPS']}")

    return requests.get(url, headers=headers, proxies=proxies)
