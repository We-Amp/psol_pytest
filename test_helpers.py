from copy import copy
import urllib3
import test_fixtures
import time
import sys

from wsgiref.handlers import format_date_time
from time import mktime

# TODO(oschaaf):
http = urllib3.PoolManager()

def get_url(url, requestHeaders = {}, log=True, userAgent = None):
  copyRequestHeaders = copy(requestHeaders)
  if "User-Agent" in requestHeaders:
    print requestHeaders["User-Agent"]
    assert userAgent is None
  else:
    if userAgent is None:
      userAgent = test_fixtures.DEFAULT_USER_AGENT
    copyRequestHeaders["User-Agent"] = userAgent

  resp = http.request('GET', url, headers=copyRequestHeaders)
  body = resp.data

  if log:
    print "get(): %s -> %s: %s (%s)" % (url, resp.status, resp.getheaders(), copyRequestHeaders)
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
    response, data = get(host, port, url, log=True, userAgent = userAgent, requestHeaders=requestHeaders)
    if predicate(response, data):
      return response, data
      break
    time.sleep(0.1)
    if time.time() > timeout_seconds:
      assert not ("Timeout waiting for predicate")

def get_until_primary(url, requestHeaders, predicate, userAgent = None):
  return get_until(test_fixtures.PRIMARY_HOST, test_fixtures.PRIMARY_PORT, url, requestHeaders, predicate, userAgent = userAgent)


# TODO(oschaaf): generic enough for all servers?
def wait_untill_nginx_accepts():
  timeout_seconds = time.time() + 5
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


