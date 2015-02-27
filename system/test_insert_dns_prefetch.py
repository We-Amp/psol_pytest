import config
import test_helpers as helpers

# Test DNS prefetching. DNS prefetching is dependent on user agent, but is
# enabled for Wget UAs, allowing this test to work with our default wget params.
def test_insert_dns_prefetch():
    filter_name = "insert_dns_prefetch"
    url = "%s/%s.html?PageSpeedFilters=%s" % (
        config.EXAMPLE_ROOT, filter_name, filter_name)
    helpers.get_until_primary(url,
        lambda resp, body: body.count("//ref.pssdemos.com") == 2)
    helpers.get_until_primary(url,
        lambda resp, body: body.count("//ajax.googleapis.com") == 2)

