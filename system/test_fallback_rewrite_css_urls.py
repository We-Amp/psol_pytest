import pytest
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_fallback_rewrite_css_urls_works(systemTestFixture):
  file = 'fallback_rewrite_css_urls.html?PageSpeedFilters=fallback_rewrite_css_urls,rewrite_css,extend_cache'
  url = "%s/%s" % (test_fixtures.EXAMPLE_ROOT, file)

  # image cache extended
  resp, body = helpers.get_until_primary(url, {}, \
    lambda response, body: body.count("Cuppa.png.pagespeed.ce.") == 1)
  assert body.count("fallback_rewrite_css_urls.css.pagespeed.cf.") == 1
  # Test this was fallback flow -> no minification.
  assert body.count("body { background") == 1
