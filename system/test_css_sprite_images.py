import re

import config
import test_helpers as helpers


def test_inline_css_rewrite_css_sprite_images_sprites_images_in_css():
    page = ("sprite_images.html?PageSpeedFilters=inline_css,rewrite_css,"
        "sprite_images")
    url = "%s/%s" % (config.EXAMPLE_ROOT, page)

    pattern = r'Cuppa.png.*BikeCrashIcn.png.*IronChef2.gif.*.pagespeed.is.*.png'
    helpers.get_until_primary(url,  lambda _resp, body: len(
            re.findall(
                pattern,
                body)) == 1)


def test_rewrite_css_sprite_images_sprites_images_in_css():
    page = "sprite_images.html?PageSpeedFilters=rewrite_css,sprite_images"
    url = "%s/%s" % (config.EXAMPLE_ROOT, page)
    _resp, body = helpers.get_until_primary(
        url, lambda _resp, body: body.count("css.pagespeed.cf") == 1)

    # Extract out the rewritten CSS file from the HTML saved by fetch_until
    # above (see -save and definition of fetch_until).  Fetch that CSS
    # file and look inside for the sprited image reference (ic.pagespeed.is...).
    results = re.findall(
        r'styles/A\.sprite_images\.css\.pagespeed\.cf\..*\.css',
        body)

    # If PreserveUrlRelativity is on, we need to find the relative URL and
    # absolutify it ourselves.
    results = [
        x if x.count("http://") == 1 else (
            "http://%s:%s%s/%s" %
            (config.PRIMARY_HOST,
             config.PRIMARY_PORT,
             config.EXAMPLE_ROOT,
             x)) for x in results]

    assert len(results) == 1
    css_url = results[0]

    print "css_url: %s" % css_url
    assert helpers.get_url(css_url).body.count("ic.pagespeed.is") > 0
