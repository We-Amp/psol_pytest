import pytest
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_combine_css_combines_4_CSS_files_into_1(systemTestFixture):
  url="%s/combine_css.html?PageSpeedFilters=combine_css" % test_fixtures.EXAMPLE_ROOT
  helpers.get_until_primary(url, {}, lambda response, body: body.count("text/css") == 1)

def test_combine_css_without_hash_field_should_404(systemTestFixture):
  url= "%s/styles/yellow.css+blue.css.pagespeed.cc..css" % test_fixtures.REWRITTEN_ROOT
  resp, body  =helpers.get_primary(url, {})
  assert resp.status == 404

def test_fetch_large_css_combine_url(systemTestFixture):
  url="%s/styles/yellow.css+blue.css+big.css+" \
    "bold.css+yellow.css+blue.css+big.css+bold.css+yellow.css+blue.css+" \
    "big.css+bold.css+yellow.css+blue.css+big.css+bold.css+yellow.css+blue.css+" \
    "big.css+bold.css+yellow.css+blue.css+big.css+bold.css+yellow.css+blue.css+" \
    "big.css+bold.css+yellow.css+blue.css+big.css+bold.css+yellow.css+blue.css+" \
    "big.css+bold.css+yellow.css+blue.css+big.css+bold.css+yellow.css+blue.css+" \
    "big.css+bold.css+yellow.css+blue.css+big.css+bold.css+yellow.css+blue.css+" \
    "big.css+bold.css+yellow.css+blue.css+big.css+bold.css+yellow.css+blue.css+" \
    "big.css+bold.css+yellow.css+blue.css+big.css+bold.css+yellow.css+blue.css+" \
    "big.css+bold.css+yellow.css+blue.css+big.css+" \
    "bold.css.pagespeed.cc.46IlzLf_NK.css" % test_fixtures.REWRITTEN_ROOT

  resp, body  =helpers.get_primary(url, {})
  assert resp.status == 200
  assert len(body.splitlines()) > 900

def test_combine_javascript_combines_2_JS_files_into_1(systemTestFixture):
  url="%s/combine_javascript.html?PageSpeedFilters=combine_javascript" % test_fixtures.EXAMPLE_ROOT
  helpers.get_until_primary(url, {}, lambda response, body: body.count("src=") == 1)

def test_combine_javascript_with_long_URL_still_works(systemTestFixture):
  url="%s/combine_js_very_many.html?PageSpeedFilters=combine_javascript" % test_fixtures.TEST_ROOT
  helpers.get_until_primary(url, {}, lambda response, body: body.count("src=") == 4)

def test_combine_heads_combines_2_heads_into_1(systemTestFixture):
  url="%s/combine_heads.html?PageSpeedFilters=combine_heads" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  assert body.count("<head>") == 1

def test_combine_css_debug_filter(systemTestFixture):
  url="%s/combine_css_debug.html?PageSpeedFilters=combine_css,debug" % test_fixtures.EXAMPLE_ROOT
  helpers.get_until_primary(url, {}, lambda response, body: body.count("styles/yellow.css+blue.css+big.css+bold.css.pagespeed.cc") == 1)
  resp, body = helpers.get_primary(url, {})
  assert body.count("potentially non-combinable attribute: &#39;id&#39;") > 0
  assert body.count("potentially non-combinable attributes: &#39;data-foo&#39; and &#39;data-bar&#39;") > 0
  assert body.count("attributes: &#39;data-foo&#39;, &#39;data-bar&#39; and &#39;data-baz&#39;") > 0
  assert body.count("looking for media &#39;&#39; but found media=&#39;print&#39;.") > 0
  assert body.count("looking for media &#39;print&#39; but found media=&#39;&#39;.") > 0
  assert body.count("Could not combine over barrier: noscript") > 0
  assert body.count("Could not combine over barrier: inline style") > 0
  assert body.count("Could not combine over barrier: IE directive") > 0

