import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def  test_convert_meta_tags(systemTestFixture):
  url = "%s/convert_meta_tags.html?PageSpeedFilters=convert_meta_tags" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  content_type = resp.getheader("content-type")
  assert content_type
  assert content_type.count("text/html;") > 0
  assert content_type.count("charset=UTF-8") > 0
