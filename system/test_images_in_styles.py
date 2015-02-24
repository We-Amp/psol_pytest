import re

import config
import test_helpers as helpers



# Rewrite images in styles.
def test_rewrite_images_rewrite_css_rewrite_style_attributes_with_url():
    page = ("rewrite_style_attributes.html?PageSpeedFilters="
        "rewrite_images,rewrite_css,rewrite_style_attributes_with_url")
    url = "%s/%s" % (config.EXAMPLE_ROOT, page)

    helpers.get_until_primary(url,
        lambda _resp, body: body.count("BikeCrashIcn.png.pagespeed.ic.") == 1)

    # TODO(oschaaf):?
    # check run_wget_with_args $URL

# Now check that it can handle two of the same image in the same style block:
def test_two_images_in_the_same_style_block():
    page = ("rewrite_style_attributes_dual.html?PageSpeedFilters="
            "rewrite_images,rewrite_css,rewrite_style_attributes_with_url")
    url = "%s/%s" % (config.EXAMPLE_ROOT, page)
    pattern = r'BikeCrashIcn.png.pagespeed.ic.*BikeCrashIcn.png.pagespeed.ic'
    helpers.get_until_primary(url,
        lambda _resp, body: len(re.findall(pattern, body)) == 1)

    # TODO(oschaaf):?
    # check run_wget_with_args $URL
