import logging
import random
import subprocess
import time
from sys import platform
from typing import List, Optional, Union

from orb.utils.decorators import retry_on_failure, timeout

log = logging.getLogger(__name__)


class VPNConnectionError(Exception):
    """
    Custom exception for errors during VPN connection or IP address change.
    """
    def __init__(self, message: str):
        super().__init__(message)


class PiaVpn:
    """
    A class for interacting with Private Internet Access (PIA) VPN.
    Assumes the PIA executable is installed on the user's system and the user has valid credentials and is logged in.
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
        else:
            log.error("Unsupported operating system. PIA executable path not set.")
            raise VPNConnectionError("Unsupported operating system for PIA VPN.")

    @property
    def get_current_region(self) -> str:
        """
        Get the currently selected region.

        Returns:
            str: The currently selected region (or "auto").

        Raises:
            RuntimeError: If the VPN is not connected.
        """
        try:
            if not self.vpn_status(as_bool=True):
                log.debug("VPN is not connected. Connecting to random region")
                self.connect()
                self._wait_for_connect()
            command = [self.piapath, "get", "region"]
            output = subprocess.check_output(command, text=True).strip()
            return output
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to get current VPN region: {e}")
            raise VPNConnectionError("Failed to get current VPN region.") from e

    @property
    def get_available_regions(self) -> List[str]:
        """
        Get a list of all available regions.

        Returns:
            List[str]: A list of available regions.
        """
        try:
            command = [self.piapath, "get", "regions"]
            output = subprocess.check_output(command, text=True).strip()
            return output.splitlines()
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to get available VPN regions: {e}")
            raise VPNConnectionError("Failed to get available VPN regions.") from e

    def set_region(self, region: Optional[str] = None) -> None:
        """
        Set the VPN region.

        Args:
            region (str, optional): The desired region. Defaults to None.

        Raises:
            ValueError: If the provided region does not exist.
            VPNConnectionError: If the VPN connection or command fails.
        """
        try:
            if not self.vpn_status(as_bool=True):
                log.info("VPN was not connected, starting up and changing regions")
                self.connect()
                if not region:
                    return

            available_regions = self.get_available_regions

            if region:
                if region.lower() not in available_regions:
                    raise ValueError("Server region provided does not exist.")
                server = region
            else:
                server = random.choice(available_regions)

            log.info(f"Setting VPN to {server} server.")
            command = [self.piapath, "set", "region", server]
            subprocess.check_output(command, text=True).strip()

            self._wait_for_connect()
            log.info(f"VPN region successfully set to {server}.")

        except subprocess.CalledProcessError as e:
            log.error(f"Failed to set VPN region to {region}: {e}")
            raise VPNConnectionError(f"Failed to set VPN region to {region}.") from e

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
            VPNConnectionError: If the VPN command fails.
        """
        try:
            command = [self.piapath, "get", "connectionstate"]
            output = subprocess.check_output(command, text=True).strip()

            if as_bool:
                return output == "Connected"
            return output
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to get VPN connection status: {e}")
            raise VPNConnectionError("Failed to get VPN connection status.") from e

    @property
    def vpn_ip(self) -> str:
        """
        Get the VPN IP address.

        Returns:
            str: The VPN IP address.

        Raises:
            VPNConnectionError: If the VPN command fails.
        """
        try:
            command = [self.piapath, "get", "vpnip"]
            output = subprocess.check_output(command, text=True).strip()
            return output
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to get VPN IP address: {e}")
            raise VPNConnectionError("Failed to get VPN IP address.") from e

    @property
    def public_ip(self) -> str:
        """
        Get the public IP address.

        Returns:
            str: The public IP address.

        Raises:
            VPNConnectionError: If the VPN command fails.
        """
        try:
            command = [self.piapath, "get", "pubip"]
            output = subprocess.check_output(command, text=True).strip()
            return output
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to get public IP address: {e}")
            raise VPNConnectionError("Failed to get public IP address.") from e

    @retry_on_failure(max_retries=1)
    @timeout(seconds=10)
    def _wait_for_connect(self) -> None:
        """
        Helper function that waits until the VPN status is 'Connected'.

        Raises:
            VPNConnectionError: If connection times out or fails.
        """
        try:
            status = self.vpn_status(as_bool=True)
            while not status:
                time.sleep(1)
                status = self.vpn_status(as_bool=True)
        except VPNConnectionError as e:
            log.error(f"Failed to connect to VPN: {e}")
            raise

    def rotate_vpn(self):
        """
        Rotate the VPN to a random region.
        """
        try:
            current_region = self.get_current_region
            self.set_region(region=None)

            self._wait_for_connect()

            new_region = self.get_current_region

            log.info(f"VPN has changed from {current_region} to {new_region}")

        except VPNConnectionError as e:
            log.error(f"Failed to rotate VPN: {e}")
            raise

    @retry_on_failure(max_retries=2)
    @timeout(seconds=10)
    def connect(self):
        """
        Connect to the VPN.

        Raises:
            VPNConnectionError: If the VPN command fails.
        """
        try:
            if self.vpn_status(as_bool=True):
                log.info(f"VPN server is already connected to {self.get_current_region} region")
                return

            command = [self.piapath, "connect"]
            subprocess.check_output(command, text=True).strip()

            self._wait_for_connect()

            log.info(f"VPN connected to {self.get_current_region} region.")
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to connect to VPN: {e}")
            raise VPNConnectionError("Failed to connect to VPN.") from e

    @retry_on_failure(max_retries=2)
    @timeout(seconds=10)
    def disconnect(self):
        """
        Disconnect from the VPN.

        Raises:
            VPNConnectionError: If the VPN command fails.
        """
        try:
            command = [self.piapath, "disconnect"]
            subprocess.check_output(command, text=True).strip()
            log.info("VPN has been disconnected.")
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to disconnect from VPN: {e}")
            raise VPNConnectionError("Failed to disconnect from VPN.") from e
