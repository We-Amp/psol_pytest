import pytest
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures


def test_canonicalize_javascript_libraries_finds_library_urls(systemTestFixture):
  # Checks that we can correctly identify a known library url.
  url = "%s/canonicalize_javascript_libraries.html?PageSpeedFilters=canonicalize_javascript_libraries" % (test_fixtures.EXAMPLE_ROOT)
  helpers.get_until_primary(url, {},
    lambda response, body: body.count("http://www.modpagespeed.com/rewrite_javascript.js") == 1)
