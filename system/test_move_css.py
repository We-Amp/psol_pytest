import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_move_css_above_scripts_works(systemTestFixture):
  url="%s/move_css_above_scripts.html?PageSpeedFilters=move_css_above_scripts" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  # Link moved before script.
  assert body.count("styles/all_styles.css\"><script") > 0

def test_move_css_above_scripts_off(systemTestFixture):
  url="%s/move_css_above_scripts.html?PageSpeedFilters=" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  # Link not moved before script.
  assert body.count("styles/all_styles.css\"><script") == 0

def test_move_css_to_head_does_what_it_says_on_the_tin(systemTestFixture):
  url="%s/move_css_to_head.html?PageSpeedFilters=move_css_to_head" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  # Link moved to head.
  assert body.count("styles/all_styles.css\"></head>") > 0

def test_move_css_to_head_off(systemTestFixture):
  url="%s/move_css_to_head.html?PageSpeedFilters=" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  # Link moved to head.
  assert body.count("styles/all_styles.css\"></head>") == 0
