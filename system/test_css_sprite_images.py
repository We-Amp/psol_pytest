import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_inline_css_rewrite_css_sprite_images_sprites_images_in_css(systemTestFixture):
  file = "sprite_images.html?PageSpeedFilters=inline_css,rewrite_css,sprite_images"
  url = "%s/%s" % (test_fixtures.EXAMPLE_ROOT, file)

  pattern = r'Cuppa.png.*BikeCrashIcn.png.*IronChef2.gif.*.pagespeed.is.*.png'
  helpers.get_until_primary(url, {}, lambda response, body: len(re.findall(pattern, body)) == 1)

def test_rewrite_css_sprite_images_sprites_images_in_css(systemTestFixture):
  file="sprite_images.html?PageSpeedFilters=rewrite_css,sprite_images"
  url = "%s/%s" % (test_fixtures.EXAMPLE_ROOT, file)
  resp, body = helpers.get_until_primary(url, {}, \
    lambda response, body: body.count("css.pagespeed.cf") == 1)

  # Extract out the rewritten CSS file from the HTML saved by fetch_until
  # above (see -save and definition of fetch_until).  Fetch that CSS
  # file and look inside for the sprited image reference (ic.pagespeed.is...).
  results = re.findall(r'styles/A\.sprite_images\.css\.pagespeed\.cf\..*\.css', body)

  # If PreserveUrlRelativity is on, we need to find the relative URL and
  # absolutify it ourselves.
  results = [x if x.count("http://") == 1 else ("http://%s:%s%s/%s" % (test_fixtures.PRIMARY_HOST, test_fixtures.PRIMARY_PORT, test_fixtures.EXAMPLE_ROOT, x)) for x in results]

  assert len(results) == 1
  css_url = results[0]

  print "css_url: %s" % css_url
  css_resp, css_body = helpers.get_url(css_url)
  assert css_body.count("ic.pagespeed.is") > 0
