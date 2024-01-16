import logging
import random
import subprocess
from sys import platform
from typing import List, Union, Optional

from orb.utils.decorators import retry_on_failure, timeout

log = logging.getLogger(__name__)


class PiaVpn:
    """
    A class for interacting with Private Internet Access (PIA) VPN.
    Class assumes the PIA executable is installed on the users system and the user has valid credentials and is logged in.
    Software can be downloaded from privateinternetaccess.com/download

    Attributes:
        piapath (str): The path to the PIA control executable.

    Methods:
        get_current_region: Get the currently selected region.
        get_available_regions: Get a list of all available regions.
        set_region: Set the VPN region.
        vpn_status: Get the VPN connection status.
        get_vpn_ip: Get the VPN IP address.
        get_public_ip: Get the public IP address.
        connect: Connect to the VPN.
        disconnect: Disconnect from the VPN.
    """

    def __init__(self, executable_path: Optional[str] = None) -> None:
        """
        Initialize the PiaVpn class.

        Sets the default piapath based on the operating system.
        """
        self.__init_executable_path(executable_path=executable_path)

    def __init_executable_path(self, executable_path: str):
        if executable_path:
            self.piapath = executable_path
        elif platform == "win32":
            self.piapath = "C:\\Program Files\\Private Internet Access\\piactl.exe"
        elif platform == "linux":
            self.piapath = "piactl"

    def get_current_region(self) -> str:
        """
        Get the currently selected region.

        Returns:
            str: The currently selected region (or "auto").

        Raises:
            RuntimeError: If the VPN is not connected.
        """
        if not self.vpn_status(as_bool=True):
            raise RuntimeError("VPN is not connected. Call connect method first")

        command = [self.piapath, "get", "region"]
        output = subprocess.check_output(command, text=True).strip()

        return output

    def get_available_regions(self) -> List[str]:
        """
        Get a list of all available regions.

        Returns:
            List[str]: A list of available regions.
        """
        command = [self.piapath, "get", "regions"]
        output = subprocess.check_output(command, text=True).strip()

        return output.splitlines()

    def set_region(self, region: Optional[str] = None) -> None:
        """
        Set the VPN region.

        Args:
            region (str, optional): The desired region. Defaults to None.

        Raises:
            ValueError: If the provided region does not exist.
            RuntimeError: If the VPN is not connected.
        """
        if not self.vpn_status(as_bool=True):
            log.info("VPN was not connected, starting up and changing regions")
            self.connect()

        available_regions = self.get_available_regions()

        if not region or region.lower() == "auto":
            server = "auto"
        elif region.lower() == "random":
            server = random.choice(available_regions)
        elif region.lower() not in available_regions:
            raise ValueError("Server region provided does not exist.")
        else:
            server = region

        log.info(f"Setting VPN to {server} server.")
        command = [self.piapath, "set", "region", server]
        subprocess.check_output(command, text=True).strip()

    def vpn_status(self, as_bool: Optional[bool] = False) -> Union[str, bool]:
        """
        Get the VPN connection status.

        Args:
            as_bool (bool, optional): Whether to return the status as a boolean.
                Defaults to False.

        Returns:
            Union[str, bool]: The VPN connection status. If `as_bool` is True,
                it returns True for "Connected" and False for other states.

        Raises:
            RuntimeError: If the VPN command fails.
        """
        command = [self.piapath, "get", "connectionstate"]
        output = subprocess.check_output(command, text=True).strip()

        if as_bool:
            return output == "Connected"
        return output

    def get_vpn_ip(self) -> str:
        """
        Get the VPN IP address.

        Returns:
            str: The VPN IP address.

        Raises:
            RuntimeError: If the VPN command fails.
        """
        command = [self.piapath, "get", "vpnip"]
        output = subprocess.check_output(command, text=True).strip()

        return output

    def get_public_ip(self) -> str:
        """
        Get the public IP address.

        Returns:
            str: The public IP address.

        Raises:
            RuntimeError: If the VPN command fails.
        """
        command = [self.piapath, "get", "pubip"]
        output = subprocess.check_output(command, text=True).strip()

        return output

    @retry_on_failure(max_retries=2)
    @timeout(seconds=10)
    def connect(self):
        """
        Connect to the VPN.

        Raises:
            RuntimeError: If the VPN command fails.
        """
        if self.vpn_status(as_bool=True):
            log.info(
                f"VPN server is already connected to {self.get_current_region()} region")
            return

        command = [self.piapath, "connect"]
        subprocess.check_output(command, text=True).strip()
        log.info(f"VPN connected to {self.get_current_region()} region.")

    @retry_on_failure(max_retries=2)
    @timeout(seconds=10)
    def disconnect(self):
        """
        Disconnect from the VPN.

        Raises:
            RuntimeError: If the VPN command fails.
        """
        command = [self.piapath, "disconnect"]
        subprocess.check_output(command, text=True).strip()
        log.info("VPN has been disconnected.")
