import logging
import os
from importlib.metadata import PackageNotFoundError, version

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_PATH = os.path.dirname(MODULE_PATH)

try:
    __version__ = version("orb-weaver")
except PackageNotFoundError:
    __version__ = "0.0.0"

log = logging.getLogger("orb")
log.addHandler(logging.NullHandler())
