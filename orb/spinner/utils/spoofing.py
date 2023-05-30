import logging
import random

from selenium import webdriver

log = logging.getLogger(__name__)


class DriverSpoofing:
    """
    A class for performing driver spoofing operations.
    """

    @staticmethod
    def change_viewport_size(
        driver: webdriver.Chrome,
        width: int = random.randint(1600, 1700),
        height: int = random.randint(800, 900)
    ) -> webdriver.Chrome:
        """
        Changes viewport size of Chrome driver to specified width and height.

        Args:
            driver (webdriver.Chrome):
                The Chrome driver instance.
            width (int, optional):
                The desired width of the viewport.
                Defaults to a random value between 1600 and 1700.
            height (int, optional):
                The desired height of the viewport.
                Defaults to a random value between 800 and 900.

        Returns:
            webdriver.Chrome: The modified Chrome driver instance.
        """
        driver.set_window_size(width=width, height=height)
        log.info(f"Driver window size reset to (h{height}, w{width})")

        return driver
