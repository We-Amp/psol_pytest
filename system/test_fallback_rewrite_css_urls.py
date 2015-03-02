import config
import test_helpers as helpers

def test_fallback_rewrite_css_urls_works():
    page = ("fallback_rewrite_css_urls.html?PageSpeedFilters="
      "fallback_rewrite_css_urls,rewrite_css,extend_cache")
    url = "%s/%s" % (config.EXAMPLE_ROOT, page)

    # image cache extended
    result, success = helpers.FetchUntil(url).waitFor(
        helpers.stringCountEquals, "Cuppa.png.pagespeed.ce.", 1)
    assert success, result.body
    body = result.body
    assert body.count("fallback_rewrite_css_urls.css.pagespeed.cf.") == 1
    # Test this was fallback flow -> no minification.
    assert body.count("body { background") == 1
