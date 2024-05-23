import random
from typing import Dict

from fake_useragent import UserAgent


class GetUserAgent:
    """
    A class for retrieving random User-Agent headers for web scraping.
    """

    def __init__(self) -> None:
        """
        Initializes the GetUserAgent object.
        Sets up the UserAgent instance.
        """
        self.user_agent = UserAgent()
        self.accept_languages = ["en-US", "en-GB", "fr-FR", "es-ES"]
        self.referer_urls = [
            "https://www.google.com",
            "https://www.bing.com",
            "https://search.yahoo.com",
            "https://en.wikipedia.org",
            "https://www.reddit.com",
            "https://twitter.com",
            "https://www.facebook.com",
            "https://www.youtube.com",
            "https://www.amazon.com",
            "https://www.cnn.com",
            "https://www.bbc.com",
            "https://www.reuters.com",
        ]

    def get_random_referer(self) -> str:
        """
        Returns a random referer URL.

        Returns:
            str: A randomly chosen referer URL.
        """
        return random.choice(self.referer_urls)

    @property
    def headers_dict(self) -> Dict[str, "UserAgent"]:
        """
        Returns a dictionary containing the User-Agent header.

        Returns:
            dict: A dictionary with the 'User-Agent' key, random user agent, and a randomly chosen referer URL.
        """
        headers = {
            "User-Agent": self.user_agent.random,
            "Accept-Language": random.choice(self.accept_languages),
            "Referer": self.get_random_referer(),
            "Cache-Control": "max-age=0" if random.random() < 0.5 else "no-cache",
            "Upgrade-Insecure-Requests": "1" if random.random() < 0.5 else "0",
            "DNT": "1" if random.random() < 0.3 else "0",
            "X-Forwarded-For": ".".join(str(random.randint(0, 255)) for _ in range(4)),
            "X-Requested-With": "XMLHttpRequest" if random.random() < 0.5 else "",
            "X-Frame-Options": "DENY" if random.random() < 0.5 else "SAMEORIGIN",
            "Connection": "keep-alive" if random.random() < 0.8 else "close",
        }
        return headers
