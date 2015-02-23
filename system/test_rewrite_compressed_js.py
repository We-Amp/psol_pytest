import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures

def test_rewrite_javascript_inline_javascript_with_gzipped_js_origin(systemTestFixture):
  print """Testing whether we can rewrite javascript resources that are served
gzipped, even though we generally ask for them clear.  This particular
js file has "alert('Hello')" but is checked into source control in gzipped
format and served with the gzip headers, so it is decodable.  This tests
that we can inline and minify that file.
"""

  url="%s/rewrite_compressed_js.html?PageSpeedFilters=rewrite_javascript,inline_javascript" %\
    test_fixtures.TEST_ROOT

  helpers.get_until_primary(url, {},
    lambda response, body: len(re.findall("Hello'", body)) == 1)

