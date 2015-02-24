import re

import config
import test_helpers as helpers




def test_quality_of_webp_output_images():
    url = ("%s/webp_rewriting/rewrite_images.html?PageSpeedFilters="
        "convert_jpeg_to_webp,rewrite_images" % config.TEST_ROOT)
    headers = {
        "PageSpeedFilters": "rewrite_images",
        "PageSpeedImageRecompressionQuality": "75",
        "PageSpeedWebpRecompressionQuality": "65",
        "User-Agent": "webp"}

    # 2 images optimized
    _resp, body = helpers.get_until_primary(
        url, lambda _resp, body: body.count(
            "256x192xPuzzle.jpg.pagespeed.ic") == 1, headers)
    results = re.findall(r'[^"]256x192.*Puzzle.*pagespeed.ic[^"]*', body)

    # Sanity check, we should only have one result
    assert len(results) == 1

    # TODO(oschaaf): make a helper to absolutify
    results = [
        x if x.count("http://") == 1 else (
            "http://%s:%s%s/images%s" %
            (config.PRIMARY_HOST,
             config.PRIMARY_PORT,
             config.EXAMPLE_ROOT,
             x)) for x in results]

    image_resp, image_body = helpers.get_url(results[0], headers)

    # If this this test fails because the image size is 7673 bytes it means
    # that image_rewrite_filter.cc decided it was a good idea to convert to
    # progressive jpeg, and in this case it's not.  See the not above on
    # kJpegPixelToByteRatio.
    assert image_resp.status == 200
    assert image_resp.getheader("content-type") == "image/webp"
    assert len(image_body) <= 5140   # resized

    # TODO(oschaaf): original test repeats the fetch_until on the html (?!)
    image_resp, image_body = helpers.get_url(results[0], headers)
    assert image_resp.status == 200
    assert image_resp.getheader("content-type") == "image/webp"
    assert len(image_body) <= 5140   # resized
