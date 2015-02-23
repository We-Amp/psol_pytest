import pytest
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_rewrite_css_extend_cache_extends_cache_of_images_in_css(systemTestFixture):
  file="rewrite_css_images.html?PageSpeedFilters=rewrite_css,extend_cache"
  url="%s/%s" % (test_fixtures.EXAMPLE_ROOT, file)

  # image cache extended
  resp, body = helpers.get_until_primary(url, {}, \
    lambda response, body: body.count("Cuppa.png.pagespeed.ce.") == 1)
  assert body.count("rewrite_css_images.css.pagespeed.cf.") == 1
