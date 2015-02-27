import config
import test_helpers as helpers

# Test DNS prefetching. DNS prefetching is dependent on user agent, but is
# enabled for Wget UAs, allowing this test to work with our default wget params.
def test_dedup_inlined_images_inline_images():
    filter_name = "dedup_inlined_images,inline_images"
    url = "%s/dedup_inlined_images.html?PageSpeedFilters=%s" % (
        config.EXAMPLE_ROOT, filter_name)
    res = helpers.get_until_primary(url,
        lambda resp, body: body.count("inlineImg(") == 4)
    assert res.body.count("PageSpeed=noscript")
