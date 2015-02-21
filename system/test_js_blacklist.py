import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_filters_do_not_rewrite_blacklisted_javascript_files(systemTestFixture):
  url="%s/blacklist/blacklist.html?PageSpeedFilters=extend_cache,rewrite_javascript,trim_urls" % test_fixtures.TEST_ROOT
  resp, body = helpers.get_until_primary(url, {},
    lambda response, body: body.count(".js.pagespeed.") == 4)
  assert len(re.findall(r'<script src=\".*normal\.js\.pagespeed\..*\.js\">', body)) > 0
  assert len(re.findall(r'<script src=\"js_tinyMCE\.js\"></script>', body)) > 0
  assert len(re.findall(r'<script src=\"tiny_mce\.js\"></script>', body)) > 0
  assert len(re.findall(r'<script src=\"tinymce\.js\"></script>', body)) > 0
  assert len(re.findall(r'<script src=\"scriptaculous\.js\?load=effects,builder\"></script>', body)) > 0
  assert len(re.findall(r'<script src=\".*jquery.*\.js\.pagespeed\..*\.js\">', body)) > 0
  assert len(re.findall(r'<script src=\".*ckeditor\.js\">', body)) > 0
  assert len(re.findall(r'<script src=\".*swfobject\.js\.pagespeed\..*\.js\">', body)) > 0
  assert len(re.findall(r'<script src=\".*another_normal\.js\.pagespeed\..*\.js\">', body)) > 0


