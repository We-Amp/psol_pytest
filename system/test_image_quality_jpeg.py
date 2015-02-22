import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_quality_of_jpeg_output_images(systemTestFixture):
  url = "%s/image_rewriting/rewrite_images.html" % test_fixtures.TEST_ROOT
  headers = { "PageSpeedFilters":"rewrite_images", \
    "PageSpeedImageRecompressionQuality": "85", "PageSpeedJpegRecompressionQuality" : "70"}

  # 2 images optimized
  resp, body = helpers.get_until_primary(url, headers, lambda response, body: body.count(".pagespeed.ic") == 2)
  results = re.findall(r'[^"]256x192.*Puzzle.*pagespeed.ic[^"]*', body)

  # Sanity check, we should only have one result
  assert len(results) == 1

  # TODO(oschaaf): make a helper to absolutify
  results = [x if x.count("http://") == 1 else ("http://%s:%s%s/images%s" \
    % (test_fixtures.PRIMARY_HOST, test_fixtures.PRIMARY_PORT, test_fixtures.EXAMPLE_ROOT, x)) for x in results]

  image_resp, image_body = helpers.get_url(results[0], headers)

  # If this this test fails because the image size is 7673 bytes it means
  # that image_rewrite_filter.cc decided it was a good idea to convert to
  # progressive jpeg, and in this case it's not.  See the not above on
  # kJpegPixelToByteRatio.
  assert image_resp.status == 200
  assert image_resp.getheader("content-type") == "image/jpeg"
  assert len(image_body) <= 7564   # resized
