import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_filter_rewrite_css_minifies_css_and_saves_bytes(systemTestFixture):
  url = "%s/rewrite_css.html?PageSpeedFilters=rewrite_css" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  assert body.count("comment") == 0
  assert len(body) < 680 # down from 689
