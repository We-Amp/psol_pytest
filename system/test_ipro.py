import pytest
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

# This tests whether fetching "/" gets you "/index.html".  With async
# rewriting, it is not deterministic whether inline css gets
# rewritten.  That's not what this is trying to test, so we use
# ?PageSpeed=off.

def test_in_place_resource_optimization(systemTestFixture):
  # Note: we intentionally want to use an image which will not appear on
  # any HTML pages, and thus will not be in cache before this test is run.
  # (Since the system_test is run multiple times without clearing the cache
  # it may be in cache on some of those runs, but we know that it was put in
  # the cache by previous runs of this specific test.)
  url = "%s/ipro/test_image_dont_reuse.png" % test_fixtures.TEST_ROOT

  # Size between original image size and rewritten image size (in bytes).
  # Used to figure out whether the returned image was rewritten or not.
  threshold_size = 13000

  # Check that we compress the image (with IPRO).
  # Note: This requests $URL until it's size is less than $THRESHOLD_SIZE.
  helpers.get_until_primary(url, {"X-PSA-Blocking-Rewrite":"psatest"},
    lambda response, content: len(content) < threshold_size)

  # TODO(oschaaf): The original tests also looks on the disk to check the
  # fetched file. Double check why.
  resp, body = helpers.get_primary(url)

  # Check that resource is served with small Cache-Control header (since
  # we cannot cache-extend resources served under the original URL).
  # Note: tr -d '\r' is needed because HTTP spec requires lines to end in \r\n,
  # but sed does not treat that as $.
  cc = resp.getheader("Cache-Control")
  assert cc
  int_cc = int(cc.replace("max-age=",""))
  assert int_cc < 1000

  # Check that the original image is greater than threshold to begin with.
  resp, body = helpers.get_primary("%s?PageSpeed=off" % url)
  assert len(body) > threshold_size

