"""Runtime configuration helpers for Orb."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class OrbConfig:
    """Small runtime config model with env-driven defaults."""

    request_timeout: int = 15
    max_retries: int = 3
    backoff_seconds: float = 0.5
    use_proxies: bool = True
    use_user_agent: bool = True

    @classmethod
    def from_env(cls) -> "OrbConfig":
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:
            # dotenv is optional; fall back to raw environment variables.
            ...
        return cls(
            request_timeout=int(os.getenv("ORB_REQUEST_TIMEOUT", "15")),
            max_retries=int(os.getenv("ORB_MAX_RETRIES", "3")),
            backoff_seconds=float(os.getenv("ORB_BACKOFF_SECONDS", "0.5")),
            use_proxies=os.getenv("ORB_USE_PROXIES", "true").lower() == "true",
            use_user_agent=os.getenv("ORB_USE_USER_AGENT", "true").lower() == "true",
        )
