from datetime import datetime
import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures


def test_extend_cache_images_rewrites_an_image_tag(systemTestFixture):
  url="%s/extend_cache.html?PageSpeedFilters=extend_cache_images" % test_fixtures.EXAMPLE_ROOT
  helpers.get_until_primary(url, {},
    lambda response, body: len(re.findall("src.*/Puzzle[.]jpg[.]pagespeed[.]ce[.].*[.]jpg", body)) == 1)
  #echo about to test resource ext corruption...
  #test_resource_ext_corruption $URL images/Puzzle.jpg.pagespeed.ce.91_WewrLtP.jpg


def test_attempt_to_fetch_cache_extended_image_without_hash_should_404():
  url="%s/images/Puzzle.jpg.pagespeed.ce..jpg" % test_fixtures.REWRITTEN_ROOT
  resp, body = helpers.get_primary(url)
  assert resp.status == 404

def test_cache_extended_image_should_respond_304_to_an_if_modified_since():
  url="%s/images/Puzzle.jpg.pagespeed.ce.91_WewrLtP.jpg" % test_fixtures.REWRITTEN_ROOT
  now = helpers.http_date(datetime.now())
  resp, body = helpers.get_primary(url, {"If-Modified-Since" : now})
  assert resp.status == 304


def test_legacy_format_urls_should_still_work():
  url="%s/images/ce.0123456789abcdef0123456789abcdef.Puzzle,j.jpg" % test_fixtures.REWRITTEN_ROOT
  resp, body = helpers.get_primary(url)
  assert resp.status == 200