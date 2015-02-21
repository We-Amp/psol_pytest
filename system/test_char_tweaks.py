import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures


def test_collapse_whitespace_removes_whitespace_but_not_from_pre_tags(systemTestFixture):
  url = "%s/collapse_whitespace.html?PageSpeedFilters=collapse_whitespace" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  assert len(re.findall(r'^ +<', body, re.MULTILINE)) == 1

def test_pedantic_adds_default_type_attributes(systemTestFixture):
  url = "%s/pedantic.html?PageSpeedFilters=pedantic" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  assert body.count("text/javascript") > 0 # should find script type
  assert body.count("text/css") > 0        # should find style type

def test_remove_comments_removes_comments_but_not_IE_directives(systemTestFixture):
  url = "%s/remove_comments.html?PageSpeedFilters=remove_comments" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  assert body.count("removed") == 0  # comment, should not find
  assert body.count("preserved") > 0 # preserves IE directives

def test_remove_quotes_does_what_it_says_on_the_tin(systemTestFixture):
  url = "%s/remove_quotes.html?PageSpeedFilters=remove_quotes" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  # TODO(oschaaf): double check this test:
  assert len(re.findall(r'"', body, re.MULTILINE)) == 4 # 2 quoted attrs
  assert body.count("'") == 0 # no apostrophes

def test_trim_urls_makes_urls_relative(systemTestFixture):
  url = "%s/trim_urls.html?PageSpeedFilters=trim_urls" % test_fixtures.EXAMPLE_ROOT
  resp, body = helpers.get_primary(url)
  assert body.count("mod_pagespeed_example") == 0 # base dir, shouldn't find
  assert len(body) < 153 # down from 157
