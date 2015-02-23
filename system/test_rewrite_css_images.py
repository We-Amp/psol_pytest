import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_rewrite_css_rewrite_images_rewrites_and_inlines_images_in_css(systemTestFixture):
  file = ("rewrite_css_images.html?PageSpeedFilters=rewrite_css,rewrite_images"
          "&ModPagespeedCssImageInlineMaxBytes=2048")
  url = "%s/%s" % (test_fixtures.EXAMPLE_ROOT, file)

  # image inlined
  resp, body = helpers.get_until_primary(url, {}, \
    lambda response, body: body.count("data:image/png;base64") == 1)
  assert body.count("rewrite_css_images.css.pagespeed.cf.") == 1

  # TODO(oschaaf):?
  # check run_wget_with_args $URL

