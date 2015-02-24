import config
import test_helpers as helpers



# This tests whether fetching "/" gets you "/index.html".  With async
# rewriting, it is not deterministic whether inline css gets
# rewritten.  That's not what this is trying to test, so we use
# ?PageSpeed=off.

url = ("%s/styles/W.rewrite_css_images.css.pagespeed.cf.Hash.css" %
    config.REWRITTEN_ROOT)


def test_image_gets_rewritten_by_default():
    # TODO(sligocki): Replace this fetch_until with single blocking fetch once
    # the blocking rewrite header below works correctly.
    helpers.get_until_primary(
        url,
        lambda _resp, content: content.count("BikeCrashIcn.png.pagespeed.ic")
        == 1, headers = {"X-PSA-Blocking-Rewrite": "psatest"})


def test_image_not_rewritten_with_pagespeed_off():
    _resp, body = helpers.get_primary(
        url,
        {"X-PSA-Blocking-Rewrite": "psatest",
         "PageSpeedFilters": "-convert_png_to_jpeg, -recompress_png"})
    assert body.count("BikeCrashIcn.png.pagespeed.ic") == 0


def test_image_not_rewritten_with_pagespeed_off_via_query():
    # TODO(vchudnov): This test is not doing quite what it advertises. It
    # seems to be getting the cached rewritten resource from the previous
    # test case and not going into image.cc itself. Removing the previous
    # test case causes this one to go into image.cc. We should test with a
    # different resource.
    _resp, body = helpers.get_primary(
        url,
        {"X-PSA-Blocking-Rewrite": "psatest",
         "PageSpeedFilters": "-convert_png_to_jpeg,-recompress_png"})
    assert body.count("BikeCrashIcn.png.pagespeed.ic") == 0
