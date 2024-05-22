import os
from typing import Optional
import socket

import requests
from selenium.webdriver.remote.webdriver import WebDriver

from orb.spinner.utils import get_user_agent
from orb import REPO_PATH


def create_welcome_page(
    proxy_info: Optional[str] = None,
    user_agent: Optional[str] = None
) -> str:
    """
    Create a welcome page HTML content with IP, proxy, and user agent information.

    Args:
        proxy_info (str, optional): Proxy information. Defaults to None.
        user_agent (str, optional): User agent information. Defaults to None.

    Returns:
        str: The HTML content of the welcome page.
    """
    ip_information = f"""
        <h2>IP Information</h2>
        <p>Local IP Address: {get_local_ip()}</p>
        <p>Public IP Address: {get_public_ip()}</p>
    """

    proxy_info_section = f"""
        <h2>Proxy Information</h2>
        <p>Proxy: {proxy_info}</p>
    """ if proxy_info else ""

    user_agent_section = f"""
        <h2>User Agent Information</h2>
        <p>User Agent: {user_agent}</p>
    """ if user_agent else ""

    page_content = f"""
    <html>
    <body>
        <h1>Welcome to the Orb Weaver Project!</h1>
        {ip_information}
        {proxy_info_section}
        {user_agent_section}
    </body>
    </html>
    """
    return page_content


def get_local_ip() -> str:
    """
    Get the local IP address of the machine.

    Returns:
        str: The local IP address.
    """
    return socket.gethostbyname(socket.gethostname())


def get_public_ip() -> str:
    """
    Get the public IP address of the machine.

    Returns:
        str: The public IP address.
    """
    response = requests.get('https://api.ipify.org')
    return response.text


def build_welcome_page(
    driver: WebDriver,
    proxy_info: Optional[str] = None,
) -> None:
    """
    Build a welcome page using the provided WebDriver and proxy info.
    Webpage is then rendered with the active driver and subsequently deleted to not store any sensitive information locally.
    Args:
        driver (WebDriver): The WebDriver instance.
        proxy_info (str): Proxy information.
        user_agent (str, optional): User agent information. Defaults to None.
    """

    page_content = create_welcome_page(
        user_agent=get_user_agent(driver=driver),
        proxy_info=proxy_info,
    )

    file_path = f"{REPO_PATH}/proxy_info.html"
    with open(file_path, 'w') as file:
        file.write(page_content)

    driver.get(f'file://{file_path}')
    os.remove(file_path)
