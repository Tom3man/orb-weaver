import logging

import requests
from fake_useragent import UserAgent
from orb.utils.proxies import GetProxies

log = logging.getLogger(__name__)


def spoof_request(url: str) -> requests:

    """
    Function that takes as input a url and uses a random selection from the USER_AGENT_LIST list to return a request from the url.
    This is needed to avoid webscraping restrictions on certain sites by randomising the user agent.

    Example: soup1 = BeautifulSoup(--output from this--, 'html.parser')

    args:
        url - string of url
    returns:
        requests response will need to be assigned to a variable

    """

    # Get a random user agent
    user_agent = UserAgent()

    # Get random proxy
    proxies = GetProxies().proxy_dict
    log.info(f"Using proxy with https: {proxies['HTTPS']}")

    headers = {'User-Agent': user_agent.random}

    return requests.get(
        url,
        headers=headers,
        proxies=proxies
    )
