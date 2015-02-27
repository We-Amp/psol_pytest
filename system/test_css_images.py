import config
import test_helpers as helpers


def test_rewrite_css_extend_cache_extends_cache_of_images_in_css():
    page = "rewrite_css_images.html?PageSpeedFilters=rewrite_css,extend_cache"
    url = "%s/%s" % (config.EXAMPLE_ROOT, page)

    # image cache extended
    _resp, body = helpers.get_until_primary(
        url, helpers.CheckSubstringCountEquals("Cuppa.png.pagespeed.ce.", 1))
    assert body.count("rewrite_css_images.css.pagespeed.cf.") == 1
