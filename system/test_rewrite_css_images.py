import config
import test_helpers as helpers



def test_rewrite_css_rewrite_images_rewrites_and_inlines_images_in_css():
    page = ("rewrite_css_images.html?PageSpeedFilters="
        "rewrite_css,rewrite_images&ModPagespeedCssImageInlineMaxBytes=2048")
    url = "%s/%s" % (config.EXAMPLE_ROOT, page)

    # image inlined
    _resp, body = helpers.get_until_primary(
        url, lambda _resp, body: body.count("data:image/png;base64") == 1)
    assert body.count("rewrite_css_images.css.pagespeed.cf.") == 1

    # TODO(oschaaf):?
    # check run_wget_with_args $URL
