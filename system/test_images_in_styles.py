import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

# Rewrite images in styles.
def test_rewrite_images_rewrite_css_rewrite_style_attributes_with_url_optimizes_images_in_style(systemTestFixture):
  file = "rewrite_style_attributes.html?PageSpeedFilters=rewrite_images,rewrite_css,rewrite_style_attributes_with_url"
  url = "%s/%s" % (test_fixtures.EXAMPLE_ROOT, file)

  resp, body = helpers.get_until_primary(url, {}, \
    lambda response, body: body.count("BikeCrashIcn.png.pagespeed.ic.") == 1)

  # TODO(oschaaf):?
  # check run_wget_with_args $URL

# Now check that it can handle two of the same image in the same style block:
def test_two_images_in_the_same_style_block(systemTestFixture):
  file = ("rewrite_style_attributes_dual.html?PageSpeedFilters="
         "rewrite_images,rewrite_css,rewrite_style_attributes_with_url")
  url = "%s/%s" % (test_fixtures.EXAMPLE_ROOT, file)
  pattern = r'BikeCrashIcn.png.pagespeed.ic.*BikeCrashIcn.png.pagespeed.ic'
  helpers.get_until_primary(url, {},
    lambda response, body: len(re.findall(pattern, body)) == 1)

  # TODO(oschaaf):?
  # check run_wget_with_args $URL
