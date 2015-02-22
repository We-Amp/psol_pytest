import pytest
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures


def test_rewrite_images_fails_broken_image(systemTestFixture):
  url = "%s/images/xBadName.jpg.pagespeed.ic.Zi7KMNYwzD.jpg" % test_fixtures.REWRITTEN_ROOT
  resp, body = helpers.get_primary(url)
  assert resp.status == 404

def test_rewrite_images_does_not_500_on_unoptomizable_image(systemTestFixture):
  url = "%s/images/xOptPuzzle.jpg.pagespeed.ic.Zi7KMNYwzD.jpg" % test_fixtures.REWRITTEN_ROOT
  resp, body = helpers.get_primary(url)
  assert resp.status == 200

