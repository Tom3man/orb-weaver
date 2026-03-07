import logging
import os
from importlib.metadata import PackageNotFoundError, version

from orb.logging_utils import setup_logging

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.dirname(MODULE_PATH)

try:
    __version__ = version("orbweaver-tools")
except PackageNotFoundError:
    __version__ = "0.0.0"

log = logging.getLogger("orb")
log.addHandler(logging.NullHandler())

__all__ = ["MODULE_PATH", "REPO_PATH", "__version__", "log", "setup_logging"]
