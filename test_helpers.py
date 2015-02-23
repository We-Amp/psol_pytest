from copy import copy
import pprint
import urllib3
import test_fixtures
import time
import sys
import httplib

from wsgiref.handlers import format_date_time
from time import mktime
import errno
from socket import error as socket_error


# TODO(oschaaf):
http = urllib3.PoolManager()
pretty_print = pprint.PrettyPrinter(indent=4)

def get_url(url, requestHeaders = {}, log=True, userAgent = None, timeout=None):
  assert url.startswith("http")

  copyRequestHeaders = copy(requestHeaders)
  if timeout is None:
      # TODO(oschaaf): sensible defaults
      timeout = urllib3.Timeout(total=10.0)
  if "User-Agent" in requestHeaders:
    print requestHeaders["User-Agent"]
    assert userAgent is None
  else:
    if userAgent is None:
      userAgent = test_fixtures.DEFAULT_USER_AGENT
    copyRequestHeaders["User-Agent"] = userAgent

  resp = http.request('GET', url, headers=copyRequestHeaders, timeout=timeout, retries = False)
  body = resp.data

  if log:
    print "get_url(): %s -> %s (%s)" % (url, resp.status, copyRequestHeaders)
    pretty_print.pprint(resp.getheaders())
    print "^^^^^^^^^^^^^^^^^^^^^"
    print body
  return resp, body

# TODO(oschaaf): rename to get_path
def get(host, port, url, requestHeaders = {}, log = True, userAgent = None, timeout = None):
  fullurl = "http://%s:%s%s" % (host, port, url)
  return get_url(fullurl, requestHeaders, log=log, userAgent = userAgent, timeout = timeout)

def get_primary(url, requestHeaders={}, userAgent = None, timeout = None):
  return get(test_fixtures.PRIMARY_HOST, test_fixtures.PRIMARY_PORT, url, \
    requestHeaders = requestHeaders, userAgent = userAgent, timeout = timeout)


def get_until(host, port, url, requestHeaders, predicate, userAgent = None):
  fullurl = "http://%s:%s%s" % (host, port, url)
  assert not url.startswith("http")
  return get_url_until(fullurl, requestHeaders, predicate, userAgent)

def get_until_primary(url, requestHeaders, predicate, userAgent = None):
  return get_until(test_fixtures.PRIMARY_HOST, test_fixtures.PRIMARY_PORT, url, requestHeaders, predicate, userAgent = userAgent)

def get_url_until(url, requestHeaders, predicate, userAgent = None):
  print "get_until(): %s" % url
  timeout_seconds = time.time() + 5
  ok = True
  while True:
    response, data = get_url(url, log = (ok==False), userAgent = userAgent, requestHeaders=requestHeaders)

    if ok:
      if predicate(response, data):
        return response, data
    else:
      assert predicate(response, data)
      return response, data

    time.sleep(0.2)
    if time.time() > timeout_seconds:
      # TODO(oschaaf): doc about why we do this (print debug info)
      if ok == False:
        assert not "Timeout waiting for predicate"
      ok = False

# TODO(oschaaf): generic enough for all servers?
def wait_untill_nginx_accepts():
  timeout_seconds = time.time() + 5
  while True:
    try:
      print "Wait until server is ready to handle requests"
      response, data = get_primary("/")
      print "Server ready"
      return
    except urllib3.exceptions.MaxRetryError as retry_err:
      if isinstance(retry_err.reason, socket_error):
        if retry_err.reason.errno != errno.ECONNREFUSED:
          # Not the error we are looking for, re-raise
          raise retry_err
        # Connection still refused, sleep and try again.
        if time.time() > timeout_seconds:
          # TODO(oschaaf): raise something more specific
          raise Exception("wait_untill_nginx_accepts timed out")
        time.sleep(0.5)
      else:
        raise

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


