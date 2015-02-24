import re
# TODO(oschaaf): dependency
import urllib3

import config
import test_helpers as helpers


def test_rewrite_javascript_minifies_javascript_and_saves_bytes():
    url = ("%s/rewrite_javascript.html?PageSpeedFilters=rewrite_javascript" %
        config.EXAMPLE_ROOT)
    pattern = r'src=.*rewrite_javascript\.js\.pagespeed\.jm\.'
    # External scripts rewritten.
    _resp, body = helpers.get_until_primary(
        url, lambda _resp, body: len(re.findall(pattern, body)) == 2)

    results = re.findall(r'".*.pagespeed.jm[^"]*', body)
    results = [x[1:] for x in results]
    # If PreserveUrlRelativity is on, we need to find the relative URL and
    # absolutify it ourselves.
    results = [
        x if x.count("http://") == 1 else (
            "http://%s:%s%s/%s" %
            (config.PRIMARY_HOST,
             config.PRIMARY_PORT,
             config.EXAMPLE_ROOT,
             x)) for x in results]

    for result in results:
        print result
        js_resp, js_body = helpers.get_url(result)
        assert js_body.count("removed") == 0  # No comments should remain.
        # Rewritten JS is cache-extended.
        assert js_resp.getheader("cache-control") == "max-age=31536000"
        assert js_resp.getheader("expires")

    assert len(body) < 1560             # Net savings
    assert body.count("preserved") > 0  # Preserves certain comments.


def test_rewrite_javascript_external():
    url = ("%s/rewrite_javascript.html?PageSpeedFilters="
        "rewrite_javascript_external" % config.EXAMPLE_ROOT)
    pattern = r'src=.*rewrite_javascript\.js\.pagespeed\.jm\.'
    _resp, body = helpers.get_until_primary(
        url, lambda _resp, body: len(re.findall(pattern, body)) == 2)
    assert body.count("// This comment will be removed") > 0


def test_rewrite_javascript_inline():
    url = ("%s/rewrite_javascript.html?PageSpeedFilters="
        "rewrite_javascript_inline" % config.EXAMPLE_ROOT)
    # We test with blocking rewrites here because we are trying to prove
    # we will never rewrite the external JS, which is impractical to do
    # with fetch_until.
    _resp, body = helpers.get_primary(url,
        {"X-PSA-Blocking-Rewrite": "psatest"})
    # Checks that the inline JS block was minified.
    assert body.count("// This comment will be removed") == 0
    assert body.count('id="int1">var state=0;document.write') > 0
    # Checks that the external JS links were left alone.
    assert body.count('src="rewrite_javascript.js') == 2
    pattern = r'src=.*rewrite_javascript\.js\.pagespeed\.jm\.'
    assert len(re.findall(pattern, body)) == 0

# Error path for fetch of outlined resources that are not in cache leaked
# at one point of development.


def test_regression_test_for_RewriteDriver_leak():
    url = "%s/_.pagespeed.jo.3tPymVdi9b.js" % config.TEST_ROOT
    result = helpers.get_primary(url)
    # TODO(oschaaf): check
    assert result.resp.status == 404

# Combination rewrite in which the same URL occurred twice used to
# lead to a large delay due to overly late lock release.


def test_regression_test_with_same_filtered_input_twice_in_combination():
    url = ("%s/_,Mco.0.css+_,Mco.0.css.pagespeed.cc.0.css?PageSpeedFilters="
        "combine_css,outline_css" % config.TEST_ROOT)
    result = helpers.get_primary(url, timeout=urllib3.Timeout(read=3.0))
    # TODO(oschaaf): test if we fail properly here.
    # We want status code 8 (server-issued error) and not 4
    # (network failure/timeout)
    assert result.resp.status == 404
