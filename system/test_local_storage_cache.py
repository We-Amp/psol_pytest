import re

import config
import test_helpers as helpers

# Force the request to be rewritten with all applicable filters.
headers = {"X-PSA-Blocking-Rewrite" : "psatest"}
pattern_img = r'<img .* alt=.A cup of joe.'
# Checks that local_storage_cache injects optimized javascript from
# local_storage_cache.js, adds the pagespeed_lsc_ attributes, inlines the data
# (if the cache were empty the inlining wouldn't make the timer cutoff but the
# resources have been fetched above).
def test_local_storage_cache_inline_css_inline_images_optimize_mode():
    filter_name = "local_storage_cache,inline_css,inline_images"
    url = "%s/local_storage_cache.html?PageSpeedFilters=%s" % (
        config.EXAMPLE_ROOT, filter_name)
    _resp, body = helpers.fetch(url, headers)
    assert body.count("pagespeed.localStorageCacheInit()")
    assert body.count(' pagespeed_lsc_url=') == 2
    assert body.count("yellow {background-color: yellow")
    assert re.search(pattern_img, body)
    assert body.count("/*") == 0
    assert body.count("PageSpeed=noscript")


# Checks that local_storage_cache,debug injects debug javascript from
# local_storage_cache.js, adds the pagespeed_lsc_ attributes, inlines the data
# (if the cache were empty the inlining wouldn't make the timer cutoff but the
# resources have been fetched above).
def test_local_storage_cache_inline_css_inline_images_debug_debug_mode():
    filter_name = "local_storage_cache,inline_css,inline_images,debug"
    url = "%s/local_storage_cache.html?PageSpeedFilters=%s" % (
        config.EXAMPLE_ROOT, filter_name)
    _resp, body = helpers.fetch(url, headers)

    assert body.count("pagespeed.localStorageCacheInit()")
    assert body.count(' pagespeed_lsc_url=') == 2
    assert body.count("yellow {background-color: yellow")
    assert body.count("<img src=\"data:image/png;base64")
    assert re.search(pattern_img, body)
    assert body.count("/*") == 0
    assert body.count("goog.require") == 0
    assert body.count("PageSpeed=noscript")


    # Checks that local_storage_cache doesn't send the inlined data for a
    # resource whose hash is in the magic cookie. First get the cookies from
    # prior runs.
    pattern = r'pagespeed_lsc_hash="([^""]*)?"'
    hashes = re.findall(pattern, body, re.MULTILINE)
    assert len(hashes) == 2
    cookie = "!".join(hashes)
    print cookie
    headers["Cookie"] = "_GPSLSC=%s" % cookie

    # Check that the prior run did inline the data.
    # TODO(oschaaf): seems like we're repeating ourselves. perhaps I missed
    # something, revisit and double check
    assert body.count("background-color: yellow")
    assert body.count("<img src=\"data:image/png;base64")
    assert re.search(pattern_img, body)

    # Fetch with the cookie set (oschaaf: and debug removed?).
    # TODO(oschaaf): somehow, in the original test, debug seems to remain on
    # even after calling test_filter without it specified. Check why that is.
    # filter_name = "local_storage_cache,inline_css,inline_images"
    # url = "%s/local_storage_cache.html?PageSpeedFilters=%s" % (
    #    config.EXAMPLE_ROOT, filter_name)

    _resp, body = helpers.fetch(url, headers)
    #print body
    # Check that this run did NOT inline the data.

    assert body.count("yellow {background-color: yellow") == 0
    assert body.count("<img src=\"data:image/png;base64") == 0

    # Check that this run inserted the expected scripts.
    script_pattern = (r'pagespeed.localStorageCache.inlineCss\(.'
        'http://.*/styles/yellow.css.\);')
    assert re.search(script_pattern, body, re.MULTILINE)

    search_pattern = (r'pagespeed.localStorageCache.inlineImg\('
                        '.http://.*/images/Cuppa.png., [^,]*, '
                        '.alt=A cup of joe., '
                        '.alt=A cup of joe., '
                        '.alt=A cup of joe..s ..joe..., '
                        '.alt=A cup of joe..s ..joe...\);')
    assert re.search(search_pattern, body)

