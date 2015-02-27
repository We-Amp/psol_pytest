import config
import test_helpers as helpers


headers = {"User-Agent" : "iPhone"}

# Checks that inline_preview_images injects compiled javascript
def test_inline_preview_images_optimize_mode():
    filter_name = "inline_preview_images"
    url = "%s/delay_images.html?PageSpeedFilters=%s" % (
        config.EXAMPLE_ROOT, filter_name)
    helpers.get_until_primary(url,
        lambda _resp, body: body.count("pagespeed.delayImagesInit") == 1,
        headers)
    helpers.get_until_primary(url,
        lambda  _resp, body: body.count("/*") == 0, headers)

    # TODO
    # check run_wget_with_args $URL

# Checks that inline_preview_images,debug injects from javascript
# in non-compiled mode
def test_inline_preview_images_debug_mode():
    filter_name = "inline_preview_images,debug"
    url = "%s/delay_images.html?PageSpeedFilters=%s" % (
        config.EXAMPLE_ROOT, filter_name)
    helpers.get_until_primary(url,
        lambda _resp, body: body.count("pagespeed.delayImagesInit") == 4,
        headers=headers)

    # TODO
    # check run_wget_with_args $URL
