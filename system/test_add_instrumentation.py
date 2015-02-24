import config
import test_helpers as helpers


def test_add_instrumentation_adds_two_script_tags():
    filter_name = "add_instrumentation"
    url = "%s/%s.html?PageSpeedFilters=%s" % (
        config.EXAMPLE_ROOT, filter_name, filter_name)
    assert helpers.get_primary(url).body.count("<script") == 2


def test_we_dont_add_instrumentation_if_url_params_tell_us_not_to():
    helpers.get_primary(
        "%s/add_instrumentation.html?PageSpeedFilters=" %
        config.EXAMPLE_ROOT,
        check = helpers.CheckSubstringCountEquals("<script", 0))

# http://code.google.com/p/modpagespeed/issues/detail?id=170
def test_make_sure_404s_are_not_rewritten():
    # Note: We run this in the add_instrumentation section because that is the
    # easiest to detect which changes every page
    # TODO(oschaaf): XXX
    bad_url = ("%s?PageSpeedFilters=add_instrumentation"
     % config.BAD_RESOURCE_URL)
    helpers.get_primary(bad_url,
        check = helpers.CheckSubstringCountEquals("/mod_pagespeed_beacon", 0))
