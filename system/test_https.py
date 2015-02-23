import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

# TODO(oschaaf): might not even be close to OK. revisit this laterself.
def test_simple_test_that_https_is_working(systemTestFixture):
  if test_fixtures.HTTPS_HOST:
    url = "%s/combine_css.html" % test_fixtures.HTTPS_EXAMPLE_ROOT

    # TODO(oschaaf): fix https fetch. originl used --no-check-certificate
    resp, body = helpers.get_url_until(url, {},\
      lambda response, body: len(re.findall(r'css\+', body, re.MULTILINE)) == 1)

    assert resp.getheader("X-Mod-Pagespeed") or resp.getheader("X-Page-Speed")
    expected = ('href="styles/yellow\.css+blue\.css+big\.css+bold\.css'
      '\.pagespeed\.cc\..*\.css"/>'
      )

    # TODO(oschaaf): fix https fetch. originl used --no-check-certificate
    print "Checking for combined CSS URL"
    helpers.get_url_until(\
      "%s?PageSpeedFilters=combine_css,trim_urls" % url, {},\
      lambda response, body: len(re.findall(pattern, body)) == 1)

    print "Checking for combined CSS URL without URL trimming"
    # Without URL trimming we still preserve URL relativity.
    helpers.get_url_until(\
      "%s?PageSpeedFilters=combine_css" % url, {},\
      lambda response, body: len(re.findall(pattern, body)) == 1)

