import socket
import requests


def create_welcome_page(
    proxy_info: str = None,
    user_agent: str = None
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
