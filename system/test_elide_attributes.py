import pytest
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures


def test_elide_attributes_removes_boolean_and_default_attributes(systemTestFixture):
  resp, body = helpers.filter_test("elide_attributes", "some descr", "query_params")
  assert body.count("disabled=") == 0
