"""
This script provides several methods for simulating human behavior in browser automation.
"""

import logging
import random
import time
from typing import Optional, Tuple, Union

from selenium.common.exceptions import (MoveTargetOutOfBoundsException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

log = logging.getLogger(__name__)


def get_user_agent(driver: WebDriver) -> str:
    """
    Get the user agent string of the Selenium WebDriver browser.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        str: The user agent string of the browser.
    """
    return driver.execute_script('return window.navigator.userAgent')


def slow_type(
    element: WebElement,
    text: str,
    delay: Union[float, int] = random.uniform(0.1, 0.5),
    send_keys: bool = False
):
    """
    Simulate human-like typing by sending text to an element character by character with a delay.

    Args:
        element (WebElement): The target element to type into.
        text (str): The text to be typed.
        delay (Union[float, int], optional): The delay between each character typing. Defaults to a random value
            between 0.1 and 0.5 seconds.
        send_keys (bool, optional): Whether to send an "Enter" key press after typing. Defaults to False.
    """
    for character in text:
        element.send_keys(character)
        time.sleep(delay)

    if send_keys:
        element.send_keys(Keys.ENTER)


def human_clicking(
    driver: WebDriver,
    target_element: WebElement,
    random_clicking: bool = True
):
    """
    Imitate human behavior when clicking in browser automation.

    Args:
        driver (WebDriver): The WebDriver instance.
        target_element (WebElement): The element to click.
        random_clicking (bool, optional): If True, include random mouse movements. Defaults to True.
    """

    actions = ActionChains(driver)

    # Pause before clicking
    actions.pause(random.random())

    perform_random_mouse_movements(
        driver=driver, random_clicking=random_clicking
    )

    actions.move_to_element_with_offset(
        target_element, random.uniform(0, 3), random.uniform(0, 3)
    )
    actions.pause(random.random())

    actions.perform()
    target_element.click()
    actions.reset_actions()


def perform_random_mouse_movements(
    driver: WebDriver,
    num_movements: int = 5,
    random_clicking: bool = True
):
    """
    Perform random mouse movements within the browser window.

    Args:
        driver (WebDriver): The WebDriver instance.
        num_movements (int, optional): The number of random mouse movements to perform. Defaults to 5.
    """
    actions = ActionChains(driver)

    for _ in range(num_movements):
        try:
            # Perform a random mouse movement by moving to a random offset
            actions.move_by_offset(
                random.uniform(-30, 30), random.uniform(-30, 30)
            )
            actions.perform()

            # Pause briefly after each movement
            actions.pause(random.uniform(0.5, 1.5))
        except MoveTargetOutOfBoundsException:
            continue

        # 40% chance of key press
        if random.random() < 0.4 and random_clicking:
            actions.send_keys(Keys.NULL)  # Press a null key to simulate random key press
            actions.perform()

        # Reset actions for the next movement
        actions.reset_actions()


def window_scroll(driver: WebDriver, scroll_range: tuple = (0, 100)):
    """
    Scroll randomly within the browser window.

    Args:
        driver (WebDriver): The WebDriver instance.
        scroll_range (tuple, optional): The range of scrolling in percentage (from top to bottom).
            Defaults to (0, 100).
    """
    # Get the current page height
    page_height = driver.execute_script("return document.body.scrollHeight")

    # Calculate the scrolling boundaries based on the given range
    scroll_start = int(page_height * scroll_range[0] / 100)
    scroll_end = int(page_height * scroll_range[1] / 100)

    # Randomly choose a scrolling position within the boundaries
    scroll_position = random.randint(scroll_start, scroll_end)

    # Scroll to the chosen position
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")


def change_viewport_size(
    driver: WebDriver,
    width: int = random.randint(1600, 1700),
    height: int = random.randint(800, 900)
):
    """
    Change the viewport size of the Chrome driver to the specified width and height.

    Args:
        driver (webdriver.Chrome): The Chrome driver instance.
        width (int, optional): The desired width of the viewport.
            Defaults to a random value between 1600 and 1700.
        height (int, optional): The desired height of the viewport.
            Defaults to a random value between 800 and 900.

    Returns:
        webdriver.Chrome: The modified Chrome driver instance.
    """
    driver.set_window_size(width=width, height=height)
    log.info(f"Driver window size reset to (h{height}, w{width})")


def find_element_with_retry(
    driver: WebDriver,
    locator: Tuple[By, str],
    retries: Optional[int] = 3,
    wait_time: Optional[int] = 30
) -> WebElement:
    """
    Locates a web element with retries in case of StaleElementReferenceException or TimeoutException.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        locator (Tuple[By, str]): The locator strategy and value as a tuple (e.g., (By.ID, "element_id")).
        retries (Optional[int]): Number of retry attempts if a StaleElementReferenceException occurs. Default is 3.
        wait_time (Optional[int]): Maximum wait time for each retry in seconds. Default is 30.

    Returns:
        WebElement: The located web element.

    Raises:
        TimeoutException: If the element is not found within the wait time across retries.
        StaleElementReferenceException: If the element remains inaccessible after retries.
    """
    for attempt in range(1, retries + 1):
        try:
            log.debug(f"Attempt {attempt} to locate element with locator: {locator}")
            return WebDriverWait(driver, wait_time).until(ec.presence_of_element_located(locator))
        except (StaleElementReferenceException, TimeoutException) as e:
            log.warning(f"Attempt {attempt} failed: {e.__class__.__name__} - {e}")
            if attempt == retries:
                log.error(f"Failed to locate element after {retries} attempts.")
                raise
