import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_extend_cache_with_no_cache_js_origin(systemTestFixture):
  print """
Test that we can rewrite resources that are served with
Cache-Control: no-cache with on-the-fly filters.  Tests that the
no-cache header is preserved.
"""
  url="%s/no_cache/hello.js.pagespeed.ce.0.js" % test_fixtures.REWRITTEN_TEST_ROOT

  resp, body = helpers.get_primary(url, {})
  assert body.count('Hello')
  assert resp.getheader("cache-control").count("no-cache")

def test_can_rewrite_cache_control_no_cache_resources_with_non_on_the_fly_filters(systemTestFixture):
  print """
Test that we can rewrite Cache-Control: no-cache resources with
non-on-the-fly filters.
"""
  url="%s/no_cache/hello.js.pagespeed.jm.0.js" % test_fixtures.REWRITTEN_TEST_ROOT

  resp, body = helpers.get_primary(url, {})
  assert body.count('Hello')
  assert resp.getheader("cache-control").count("no-cache")
