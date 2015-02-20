import pytest
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures


############################### tests #########################################

def test_initial_header(systemTestFixture):
  # TODO(oschaaf): branding, etc
  # TODO(oschaaf): split this up in separate tests?
  response, body = helpers.get_primary("%s/combine_css.html" % test_fixtures.EXAMPLE_ROOT)

  print "Checking for X-Mod-Pagespeed header"
  ps_server_header = response.getheader("X-Mod-Pagespeed")
  if ps_server_header is None:
      ps_server_header  = response.getheader("X-Page-Speed")

  assert (ps_server_header != None)

  print "Checking that we don't have duplicate X-Mod-Pagespeed headers"
  assert (',' not in ps_server_header)

  print "Checking that we don't have duplicate headers"
  responseHeaders = response.getheaders();
  assert(len(set(responseHeaders)) == len(responseHeaders))

  print "Checking for lack of E-tag"
  assert(not response.getheader("Etag"))

  print "Checking for presence of Vary."
  assert(response.getheader("Vary") == "Accept-Encoding")


  print "Checking for absence of Last-Modified"
  assert(not response.getheader("Last-Modified"))

  # Note: This is in flux, we can now allow cacheable HTML and this test will
  # need to be updated if this is turned on by default.
  print "Checking for presence of Cache-Control: max-age=0, no-cache"
  assert response.getheader("Cache-Control") == "max-age=0, no-cache"

  print "Checking for absence of X-Frame-Options: SAMEORIGIN"
  assert(not response.getheader("X-Frame-Options"))


def test_pagespeed_added_with_pagespeed_on(systemTestFixture):
  print "X-Mod-Pagespeed header added when PageSpeed=on"
  response, body = helpers.get_primary("%s/combine_css.html?PageSpeed=on" %  test_fixtures.EXAMPLE_ROOT)
  assert(response.getheader("X-Mod-Pagespeed") or response.getheader("X-Page-Speed") )

def test_pagespeed_not_added_with_pagespeed_off(systemTestFixture):
  print "X-Mod-Pagespeed header not added when PageSpeed=off"
  response, body = helpers.get_primary("%s/combine_css.html?PageSpeed=off" % test_fixtures.EXAMPLE_ROOT)
  assert(not response.getheader("X-Mod-Pagespeed") and not response.getheader("X-Page-Speed") )
