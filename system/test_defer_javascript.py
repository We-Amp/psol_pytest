import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_pagespeed_qs_param_insert_canonical_href_link(systemTestFixture):
  url = "%s/defer_javascript.html?PageSpeed=noscript" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  assert body.count('link rel="canonical" href="%s%s/defer_javascript.html"' %\
   (test_fixtures.PRIMARY_SERVER, test_fixtures.EXAMPLE_ROOT))

# Checks that defer_javascript injects 'pagespeed.deferJs' from defer_js.js,
# but strips the comments.
def test_defer_javascript_optimize_mode(systemTestFixture):
  url = "%s/defer_javascript.html?PageSpeedFilters=defer_javascript" %\
   test_fixtures.EXAMPLE_ROOT

  resp, body = helpers.get_primary(url)
  assert body.count("text/psajs")
  assert body.count("js_defer")
  assert body.count("PageSpeed=noscript")


# Checks that defer_javascript,debug injects 'pagespeed.deferJs' from
# defer_js.js, but retains the comments.
def test_defer_javascript_debug_optimize_mode(systemTestFixture):
  url = "%s/defer_javascript.html?PageSpeedFilters=defer_javascript,debug" %\
   test_fixtures.EXAMPLE_ROOT

  resp, body = helpers.get_primary(url)
  assert body.count("text/psajs")
  assert body.count("js_defer_debug")
  assert body.count("PageSpeed=noscript")

  # The deferjs src url is in the format js_defer.<hash>.js. This strips out
  # everthing except the js filename and saves it to test fetching later.
  # TODO(oschaaf): make sure that we need to capture the debug version
  match = re.search(r'src="/.*/(js_defer.*\.js)"', body)
  assert match
  js_defer_leaf = match.group(1)
  assert js_defer_leaf


  js_defer_url = "http://%s/%s/%s" % \
    (test_fixtures.PROXY_DOMAIN, test_fixtures.PSA_JS_LIBRARY_URL_PREFIX, js_defer_leaf)
  resp, body = helpers.get_url(js_defer_url)
  assert resp.status == 200
  assert resp.getheader("cache-control") == "max-age=31536000"


# Checks that we return 404 for static file request without hash.
def test_access_to_js_defer_js_without_hash_returns_404(systemTestFixture):
  url = "http://%s/%s/js_defer.js" % \
    (test_fixtures.PROXY_DOMAIN, test_fixtures.PSA_JS_LIBRARY_URL_PREFIX)
  resp, body = helpers.get_url(url)
  assert resp.status == 404

# Checks that outlined js_defer.js is served correctly.
def test_serve_js_defer_0_js(systemTestFixture):
  url = "http://%s/%s/js_defer.0.js" % \
    (test_fixtures.PROXY_DOMAIN, test_fixtures.PSA_JS_LIBRARY_URL_PREFIX)
  resp, body = helpers.get_url(url)
  assert resp.status == 200
  assert resp.getheader("cache-control") == "max-age=300,private"


# Checks that outlined js_defer_debug.js is  served correctly.
def test_serve_js_defer_debug_0_js(systemTestFixture):
  url = "http://%s/%s/js_defer_debug.0.js" % \
    (test_fixtures.PROXY_DOMAIN, test_fixtures.PSA_JS_LIBRARY_URL_PREFIX)
  resp, body = helpers.get_url(url)
  assert resp.status == 200
  assert resp.getheader("cache-control") == "max-age=300,private"
