import re

import config
import test_helpers as helpers



def test_rewrite_images_inlines_compresses_and_resizes():
    url = ("%s/rewrite_images.html?PageSpeedFilters=rewrite_images" %
        config.EXAMPLE_ROOT)

    # TODO(oschaaf): fetch_until and blocking rewrite??
    # Images inlined.
    helpers.get_until_primary(
        url,
        lambda _resp, body: body.count("data:image/png") == 1)
    # Images rewritten.
    helpers.get_until_primary(
        url,
        lambda _resp, body: body.count(".pagespeed.ic") == 2)

    # Verify with a blocking fetch that pagespeed_no_transform worked and was
    # stripped.
    helpers.get_until_primary(
        url,
        lambda _resp, body: body.count("images/disclosure_open_plus.png") == 1
        , headers = {"X-PSA-Blocking-Rewrite": "psatest"})

    helpers.get_until_primary(
        url,
        lambda _resp, body: body.count('"pagespeed_no_transform"') == 0,
        headers = {"X-PSA-Blocking-Rewrite": "psatest"})


def test_size_of_rewritten_image():
    url = ("%s/rewrite_images.html?PageSpeedFilters=rewrite_images" %
        config.EXAMPLE_ROOT)
    # Note: We cannot do this above because the intervening fetch_untils will
    # clean up $OUTDIR.
    _resp, body = helpers.get_until_primary(
        url,
        lambda _resp, body: body.count(".pagespeed.ic") == 2,
        headers = {"Accept-Encoding": "gzip"})
    results = re.findall(r'[^"]*.pagespeed.ic[^"]*', body)

    # If PreserveUrlRelativity is on, we need to find the relative URL and
    # absolutify it ourselves.
    results = [
        x if x.count("http://") == 1 else (
            "http://%s:%s%s/%s" %
            (config.PRIMARY_HOST,
             config.PRIMARY_PORT,
             config.EXAMPLE_ROOT,
             x)) for x in results]

    assert len(results) == 2
    _resp_img0, body_img0 = helpers.get_url(results[0])
    resp_img1, body_img1 = helpers.get_url(results[1])

    assert len(body_img0) < 25000  # re-encoded
    assert len(body_img1) < 24126  # resized

    # TODO(oschaaf): Used to "start_test headers for rewritten image" and others
    # ,which would translate to a lot of very small functions
    print resp_img1.getheaders()

    assert resp_img1.status == 200
    # Make sure we have some valid headers.
    assert resp_img1.getheader("content-type").lower() == "image/jpeg"
    # Make sure the response was not gzipped.
    assert not resp_img1.getheader("content-encoding")
    # Make sure there is no vary-encoding
    assert not resp_img1.getheader("vary")
    # Make sure there is an etag
    assert resp_img1.getheader("etag").lower() in ['w/"0"', 'w/"0-gzip"']
    # Make sure an extra header is propagated from input resource to output
    # resource.  X-Extra-Header is added in debug.conf.template.
    assert resp_img1.getheader("x-extra-header")
    # Make sure there is a last-modified tag
    assert resp_img1.getheader("last-modified")
