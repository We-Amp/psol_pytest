import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_inline_css_converts_3_out_of_5_link_tags_to_style_tags(systemTestFixture):
  url = "%s/inline_css.html?PageSpeedFilters=inline_css" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_until_primary(url, {}, lambda response, body: body.count("<style") == 3)

def test_inline_google_font_css_can_inline_google_font_api_loader_css(systemTestFixture):
  url = "%s/inline_google_font_css.html?PageSpeedFilters=inline_google_font_css" % test_fixtures.EXAMPLE_ROOT

  # TODO(oschaaf): ->don't test in that case:
  # In some test environments these tests can't be run because of
  # restrictions on external connections
  userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36"

  resp, body = helpers.get_until_primary(url, {}, lambda response, body: body.count("@font-face") == 7, userAgent=userAgent)
  lbody = body.lower()
  assert lbody.count("woff2") > 0
  assert lbody.count("format('truetype')") == 0
  assert lbody.count("embedded-opentype") == 0
  assert lbody.count(".ttf") == 0
  assert lbody.count(".eot") == 0

  # Now try with IE6 user-agent
  userAgent = "Mozilla/4.0 (compatible; MSIE 6.01; Windows NT 6.0)"
  resp, body = helpers.get_until_primary(url, {}, lambda response, body: body.count("@font-face") == 1, userAgent=userAgent)
  lbody = body.lower()

  # This should get an eot font. (It might also ship a woff, so we don't
  # check_not_from for that)
  assert lbody.count(".eot") > 0
  assert lbody.count(".ttf") == 0


def test_inline_javascript_inlines_a_small_js_file(systemTestFixture):
  url = "%s/inline_javascript.html?PageSpeedFilters=inline_javascript" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_until_primary(url, {}, lambda response, body: body.count("document.write") == 1)
