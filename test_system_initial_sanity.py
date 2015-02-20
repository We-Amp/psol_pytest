import pytest
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

# This tests whether fetching "/" gets you "/index.html".  With async
# rewriting, it is not deterministic whether inline css gets
# rewritten.  That's not what this is trying to test, so we use
# ?PageSpeed=off.

def test_directory_mapped_to_index(systemTestFixture):
  autoindex, autoIndexBody = helpers.get_primary("%s/?PageSpeed=off" % test_fixtures.EXAMPLE_ROOT)
  index, indexBody = helpers.get_primary("%s/index.html?PageSpeed=off" % test_fixtures.EXAMPLE_ROOT)
  assert indexBody == autoIndexBody

def test_compression_enabled_for_html(systemTestFixture):
  response, body = helpers.get_primary("%s/" % test_fixtures.EXAMPLE_ROOT,
        requestHeaders = {'Accept-Encoding':'gzip'})
  assert response.getheader("Content-Encoding") == "gzip"

def test_whitespace_served_as_html_behaves_sanely(systemTestFixture):
  response, body = helpers.get_primary("%s/whitespace.html" % test_fixtures.TEST_ROOT)
  assert response.status == 200
