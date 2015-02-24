import pytest

import config
import test_helpers as helpers


skip = "not config.SECONDARY_HOST"
# TODO(oschaaf): original tests use generate_url() call!

# Cookie options on: by default comments not removed, whitespace is
@pytest.mark.skipif(skip)
def test_setting_cookie_on_options_no_cookie():
    headers = {"Host": "options-by-cookies-enabled.example.com"}
    page = "/mod_pagespeed_test/forbidden.html"
    url = "%s%s" % (config.SECONDARY_SERVER, page)
    _resp, body = helpers.get_url(url, headers = headers)
    assert body.count("<!--")
    assert body.count("  ") == 0


# Cookie options on: set option by cookie takes effect
@pytest.mark.skipif(skip)
def test_setting_cookie_on_options_takes_effect():
    headers = {"Host": "options-by-cookies-enabled.example.com",
        "Cookie" : "PageSpeedFilters=%2bremove_comments"}
    page = "/mod_pagespeed_test/forbidden.html"
    url = "%s%s" % (config.SECONDARY_SERVER, page)
    _resp, body = helpers.get_url(url, headers = headers)
    assert body.count("<!--") == 0
    assert body.count("  ") == 0

# Cookie options on: set option by cookie takes effect
@pytest.mark.skipif(skip)
def test_setting_cookie_on_options_invalid_cookie_takes_no_effect():
    # The '+' must be encoded as %2b for the cookie parsing code to accept it.
    headers = {"Host": "options-by-cookies-enabled.example.com",
        "Cookie" : "PageSpeedFilters=+remove_comments"}
    page = "/mod_pagespeed_test/forbidden.html"
    url = "%s%s" % (config.SECONDARY_SERVER, page)
    _resp, body = helpers.get_url(url, headers = headers)
    assert body.count("<!--")
    assert body.count("  ") == 0


# Cookie options off: by default comments nor whitespace removed
@pytest.mark.skipif(skip)
def test_setting_cookie_on_options_no_cookie():
    headers = {"Host": "options-by-cookies-disabled.example.com"}
    page = "/mod_pagespeed_test/forbidden.html"
    url = "%s%s" % (config.SECONDARY_SERVER, page)
    _resp, body = helpers.get_url(url, headers = headers)
    assert body.count("<!--")
    assert body.count("  ")

# Cookie options off: set option by cookie has no effect
@pytest.mark.skipif(skip)
def test_setting_cookie_on_options_cookie_no_effect():
    headers = {"Host": "options-by-cookies-disabled.example.com",
        "Cookie" : "PageSpeedFilters=%2bremove_comments"}
    page = "/mod_pagespeed_test/forbidden.html"
    url = "%s%s" % (config.SECONDARY_SERVER, page)
    _resp, body = helpers.get_url(url, headers = headers)
    assert body.count("<!--")
    assert body.count("  ")
