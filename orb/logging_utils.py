"""Logging setup helper for users of the package."""

from __future__ import annotations

import logging


def setup_logging(level: int = logging.INFO, logger_name: str = "orb") -> logging.Logger:
    """Configure a stream logger once and return it."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s"))
        logger.addHandler(handler)

    return logger
