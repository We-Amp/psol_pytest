from datetime import datetime
import pytest
import re
import test_helpers as helpers
from test_fixtures import systemTestFixture
import test_fixtures


def test_extend_cache_images_rewrites_an_image_tag(systemTestFixture):
  url="%s/extend_cache.html?PageSpeedFilters=extend_cache_images" % test_fixtures.EXAMPLE_ROOT
  helpers.get_until_primary(url, {},
    lambda response, body: len(re.findall("src.*/Puzzle[.]jpg[.]pagespeed[.]ce[.].*[.]jpg", body)) == 1)
  #echo about to test resource ext corruption...
  #test_resource_ext_corruption $URL images/Puzzle.jpg.pagespeed.ce.91_WewrLtP.jpg

def test_attempt_to_fetch_cache_extended_image_without_hash_should_404(systemTestFixture):
  url="%s/images/Puzzle.jpg.pagespeed.ce..jpg" % test_fixtures.REWRITTEN_ROOT
  resp, body = helpers.get_primary(url)
  assert resp.status == 404

def test_cache_extended_image_should_respond_304_to_an_if_modified_since(systemTestFixture):
  url="%s/images/Puzzle.jpg.pagespeed.ce.91_WewrLtP.jpg" % test_fixtures.REWRITTEN_ROOT
  now = helpers.http_date(datetime.now())
  resp, body = helpers.get_primary(url, {"If-Modified-Since" : now})
  assert resp.status == 304

def test_legacy_format_urls_should_still_work(systemTestFixture):
  url="%s/images/ce.0123456789abcdef0123456789abcdef.Puzzle,j.jpg" % test_fixtures.REWRITTEN_ROOT
  resp, body = helpers.get_primary(url)
  assert resp.status == 200

# Cache extend PDFs.
def test_extend_cache_pdfs_pdf_cache_extension(systemTestFixture):
  url="%s/extend_cache_pdfs.html?PageSpeedFilters=extend_cache_pdfs" % test_fixtures.EXAMPLE_ROOT
  helpers.get_until_primary(url, {},
    lambda response, body: body.count(".pagespeed.") == 3)
  resp, body = helpers.get_primary(url)

  assert len(re.findall("a href=\".*pagespeed.*\.pdf", body)) > 0
  assert len(re.findall("embed src=\".*pagespeed.*\.pdf", body)) > 0
  assert len(re.findall("<a href=\"example.notpdf\">", body)) > 0
  assert len(re.findall("<a href=\".*pagespeed.*\\.pdf\">example.pdf\\?a=b", body)) > 0

def test_cache_extended_pdfs_load_and_have_the_right_mime_type(systemTestFixture):
  url="%s/extend_cache_pdfs.html?PageSpeedFilters=extend_cache_pdfs" % test_fixtures.EXAMPLE_ROOT
  helpers.get_until_primary(url, {},
    lambda response, body: body.count(".pagespeed.") == 3)
  resp, body = helpers.get_primary(url)
  results = re.findall(r'http://[^\"]*pagespeed.[^\"]*\.pdf', body)
  ce_url_prepend = ""
  if len(results) == 0:
    # If PreserveUrlRelativity is on, we need to find the relative URL and
    # absolutify it ourselves.
    results = re.findall(r'[^\"]*pagespeed.[^\"]*\.pdf', body)
    ce_url_prepend = test_fixtures.EXAMPLE_ROOT

  assert len(results) > 0

  ce_url = "%s/%s" % (ce_url_prepend, results[1])
  print "Extracted cache-extended url: %s" % ce_url

  resp, body = helpers.get_primary(ce_url)
  assert resp.getheader("content-type") == "application/pdf"


