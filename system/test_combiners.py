import config
import test_helpers as helpers


def test_combine_css_combines_4_CSS_files_into_1():
    url = ("%s/combine_css.html?PageSpeedFilters=combine_css" %
        config.EXAMPLE_ROOT)
    helpers.get_until_primary(
        url,
        helpers.CheckSubstringCountEquals("text/css", 1))

def test_combine_css_without_hash_field_should_404():
    url = ("%s/styles/yellow.css+blue.css.pagespeed.cc..css" %
        config.REWRITTEN_ROOT)
    assert helpers.get_primary(url).resp.status == 404


def test_fetch_large_css_combine_url():
    rep = ("big.css+bold.css+yellow.css+blue.css+big.css+bold.css+yellow.css"
        "+blue.css+")
    url = ("%s/styles/yellow.css+blue.css+big.css+"
        "bold.css+yellow.css+blue.css+big.css+bold.css+yellow.css+blue.css+"
        "%s%s%s%s%s%s%s"
        "big.css+bold.css+yellow.css+blue.css+big.css+"
        "bold.css.pagespeed.cc.46IlzLf_NK.css"
        % (config.REWRITTEN_ROOT, rep, rep, rep, rep, rep, rep, rep))

    resp, body = helpers.get_primary(url)
    assert resp.status == 200
    assert len(body.splitlines()) > 900


def test_combine_javascript_combines_2_JS_files_into_1():
    url = ("%s/combine_javascript.html?PageSpeedFilters=combine_javascript" %
        config.EXAMPLE_ROOT)
    helpers.get_until_primary(
        url,
        helpers.CheckSubstringCountEquals("src=", 1))


def test_combine_javascript_with_long_URL_still_works():
    url = ("%s/combine_js_very_many.html?PageSpeedFilters=combine_javascript" %
        config.TEST_ROOT)
    helpers.get_until_primary(url,
        helpers.CheckSubstringCountEquals("src=", 4))

def test_combine_heads_combines_2_heads_into_1():
    url = ("%s/combine_heads.html?PageSpeedFilters=combine_heads" %
        config.EXAMPLE_ROOT)
    helpers.get_primary(url,
        check = helpers.CheckSubstringCountEquals("<head>", 1))

def test_combine_css_debug_filter():
    url = ("%s/combine_css_debug.html?PageSpeedFilters=combine_css,debug" %
        config.EXAMPLE_ROOT)
    helpers.get_until_primary(
        url, lambda _resp, body: body.count(
            "styles/yellow.css+blue.css+big.css+bold.css.pagespeed.cc") == 1)
    _resp, body = helpers.get_primary(url, {})
    assert body.count("potentially non-combinable attribute: &#39;id&#39;") > 0
    assert body.count(
        ("potentially non-combinable attributes: &#39;data-foo&#39; "
        "and &#39;data-bar&#39;")) > 0
    assert body.count(
        ("attributes: &#39;data-foo&#39;, &#39;data-bar&#39; and &#39;"
        "data-baz&#39;")) > 0
    assert body.count(
        "looking for media &#39;&#39; but found media=&#39;print&#39;.") > 0
    assert body.count(
        "looking for media &#39;print&#39; but found media=&#39;&#39;.") > 0
    assert body.count("Could not combine over barrier: noscript") > 0
    assert body.count("Could not combine over barrier: inline style") > 0
    assert body.count("Could not combine over barrier: IE directive") > 0
