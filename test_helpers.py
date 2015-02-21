import urllib3
import test_fixtures
import time
import sys

from wsgiref.handlers import format_date_time
from time import mktime

def get_url(url, requestHeaders = {}, log=True, userAgent = None):
  if userAgent is None:
    # TODO(oschaaf): default user-agent
    userAgent = "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.0 (KHTML, like Gecko) Chrome/6.0.408.1 Safari/534.0"

  http = urllib3.PoolManager()

  # TODO(oschaaf): we might not always want to do this, check the system test helpers.
  requestHeaders["User-Agent"] = userAgent
  resp = http.urlopen('GET', url, headers=requestHeaders)
  body = resp.data

  if log:
    print "get(): %s -> %s: %s" % (url, resp.status, resp.getheaders())
  return resp, body

# TODO(oschaaf): rename to get_path
def get(host, port, url, requestHeaders = {}, log=True, userAgent = None):
  fullurl = "http://%s:%s%s" % (host, port, url)
  return get_url(fullurl, requestHeaders, log, userAgent)

def get_primary(url, requestHeaders={}, userAgent = None):
  return get(test_fixtures.PRIMARY_HOST, test_fixtures.PRIMARY_PORT, url, requestHeaders = requestHeaders, userAgent = userAgent)

def get_until(host, port, url, requestHeaders, predicate, userAgent = None):
  fullurl = "http://%s:%s%s" % (host, port, url)
  print "get_until(): %s" % fullurl
  timeout_seconds = time.time() + 5
  while True:
    response, data = get(host, port, url, log=False, userAgent = userAgent)
    if predicate(response, data):
      return response, data
      break
    if time.time() > timeout_seconds:
      assert not ("Timeout waiting for predicate")

def get_until_primary(url, requestHeaders, predicate, userAgent = None):
  return get_until(test_fixtures.PRIMARY_HOST, test_fixtures.PRIMARY_PORT, url, requestHeaders, predicate, userAgent = userAgent)


# TODO(oschaaf): generic enough for all servers?
def wait_untill_nginx_accepts():
  timeout_seconds = time.time() + 30
  while True:
    try:
      print "Wait until server is ready to handle requests"
      response, data = get_primary("/")
      print "Server ready"
      return
    except:
      print "except :" , sys.exc_info()[1]
      time.sleep(0.1)

    if time.time() > timeout_seconds:
      # TODO(oschaaf): raise something more specific
      raise Exception("wait_untill_nginx_accepts timed out")

# Helper to set up most filter tests.  Alternate between using:
#  1) query-params vs request-headers
#  2) ModPagespeed... vs PageSpeed...
# to enable the filter so we know all combinations work.
def filter_test(filter_name, filter_description, filter_spec_method):
  # TODO(oschaaf): mentions other args the PageSpeedFilters=
  url = "%s/%s.html?PageSpeedFilters=%s" % (test_fixtures.EXAMPLE_ROOT, filter_name, filter_name)
  resp, body = get_primary(url)
  return resp, body

def http_date(d):
  stamp = mktime(d.timetuple())
  return format_date_time(stamp)
