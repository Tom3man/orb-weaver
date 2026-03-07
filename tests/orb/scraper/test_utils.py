from unittest.mock import MagicMock, patch

from orb.config import OrbConfig
from orb.scraper.utils import spoof_request


@patch("orb.scraper.utils.request_get_with_retry")
@patch("orb.scraper.utils.GetUserAgent")
def test_spoof_request_without_proxy(mock_ua, mock_request):
    mock_ua.return_value.headers_dict = {"User-Agent": "UA"}
    mock_response = MagicMock(status_code=200)
    mock_request.return_value = mock_response

    response = spoof_request("https://example.com", use_proxies=False)

    assert response is mock_response
    mock_request.assert_called_once()


@patch("orb.scraper.utils.request_get_with_retry")
@patch("orb.scraper.utils.GetProxies")
@patch("orb.scraper.utils.GetUserAgent")
def test_spoof_request_uses_config(mock_ua, mock_proxies, mock_request):
    mock_ua.return_value.headers_dict = {"User-Agent": "UA"}
    mock_proxies.return_value.proxy_dict = {"http": "1.2.3.4:8080", "https": "1.2.3.4:8080"}
    mock_response = MagicMock(status_code=200)
    mock_request.return_value = mock_response

    config = OrbConfig(
        request_timeout=9,
        max_retries=2,
        backoff_seconds=0.1,
        use_proxies=True,
        use_user_agent=True,
    )

    spoof_request("https://example.com", config=config)

    mock_request.assert_called_once()
    _, kwargs = mock_request.call_args
    assert kwargs["timeout"] == 9
    assert kwargs["max_retries"] == 2
    assert kwargs["backoff_seconds"] == 0.1
