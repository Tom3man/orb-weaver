"""
This script provides several methods for spoofing requests.
"""

import logging

import requests

from orb.common.proxies.get_proxies import GetProxies
from orb.common.user_agents.user_agents import GetUserAgent
from orb.config import OrbConfig
from orb.net import request_get_with_retry

log = logging.getLogger(__name__)


def spoof_request(
    url: str,
    use_proxies: bool = True,
    use_user_agent: bool = True,
    timeout: int = 15,
    max_retries: int = 3,
    backoff_seconds: float = 0.5,
    config: OrbConfig | None = None,
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

    if config is not None:
        use_proxies = config.use_proxies
        use_user_agent = config.use_user_agent
        timeout = config.request_timeout
        max_retries = config.max_retries
        backoff_seconds = config.backoff_seconds

    # Get a random user agent
    if use_user_agent:
        headers = GetUserAgent().headers_dict

    # Get a random proxy
    if use_proxies:
        proxies = GetProxies().proxy_dict
        log.info(f"Using proxy with HTTPS: {proxies['https']}")

    return request_get_with_retry(
        url,
        headers=headers,
        proxies=proxies,
        timeout=timeout,
        max_retries=max_retries,
        backoff_seconds=backoff_seconds,
    )
