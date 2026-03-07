from orb.common.user_agents.user_agents import GetUserAgent


def test_get_random_referer_in_known_list():
    ua = GetUserAgent()
    referer = ua.get_random_referer()
    assert referer in ua.referer_urls


def test_headers_dict_contains_required_keys():
    headers = GetUserAgent().headers_dict
    assert "User-Agent" in headers
    assert "Accept-Language" in headers
    assert "Referer" in headers
