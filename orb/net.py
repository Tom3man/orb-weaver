"""Network helpers with bounded retries/backoff."""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

import requests


def request_get_with_retry(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    proxies: Optional[Dict[str, str]] = None,
    timeout: int = 15,
    max_retries: int = 3,
    backoff_seconds: float = 0.5,
    **kwargs: Any,
) -> requests.Response:
    """GET a URL with simple exponential backoff retry logic."""
    last_exc: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            last_exc = exc
            if attempt == max_retries:
                break
            time.sleep(backoff_seconds * (2 ** (attempt - 1)))

    if last_exc is None:
        raise RuntimeError("request_get_with_retry exhausted retries without an exception")
    raise last_exc
