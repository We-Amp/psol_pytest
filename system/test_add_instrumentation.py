import config
import test_helpers as helpers


def test_add_instrumentation_adds_two_script_tags():
    filter_name = "add_instrumentation"
    url = "%s/%s.html?PageSpeedFilters=%s" % (
        config.EXAMPLE_ROOT, filter_name, filter_name)
    assert helpers.fetch(url).body.count("<script") == 2


def test_we_dont_add_instrumentation_if_url_params_tell_us_not_to():
    result = helpers.fetch(
        "%s/add_instrumentation.html?PageSpeedFilters=" % config.EXAMPLE_ROOT)
    assert helpers.stringCountEquals(result, "<script", 0), result.body

# http://code.google.com/p/modpagespeed/issues/detail?id=170
def test_make_sure_404s_are_not_rewritten():
    # Note: We run this in the add_instrumentation section because that is the
    # easiest to detect which changes every page
    # TODO(oschaaf): XXX
    bad_url = ("%s?PageSpeedFilters=add_instrumentation"
     % config.BAD_RESOURCE_URL)
    result = helpers.fetch(bad_url, allow_error_responses = True)
    expect = "/mod_pagespeed_beacon"
    assert helpers.stringCountEquals(result, expect, 0), result.body
