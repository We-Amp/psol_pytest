import pytest
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures


def test_add_instrumentation_adds_two_script_tags(systemTestFixture):
  # TODO(oschaaf): descr
  resp, body = helpers.filter_test("add_instrumentation", "some descr", "query_params")
  assert body.count("<script") == 2

def test_we_dont_add_instrumentation_if_url_params_tell_us_not_to(systemTestFixture):
  resp, body = helpers.get_primary("%s/add_instrumentation.html?PageSpeedFilters=" % test_fixtures.EXAMPLE_ROOT)
  assert body.count("<script") == 0

# http://code.google.com/p/modpagespeed/issues/detail?id=170
def test_make_sure_404s_are_not_rewritten(systemTestFixture):
  # Note: We run this in the add_instrumentation section because that is the
  # easiest to detect which changes every page
  # TODO(oschaaf): XXX
  bad_url="%s?PageSpeedFilters=add_instrumentation" % test_fixtures.BAD_RESOURCE_URL
  resp, body = helpers.get_primary(bad_url)
  assert body.count("/mod_pagespeed_beacon") == 0

