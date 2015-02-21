import httplib
import test_fixtures
import time
import sys

def get(host, port, url, requestHeaders = {}):
  http = httplib.HTTPConnection(host, port, timeout=30)
  http.connect()
  # TODO(oschaaf): we might not always want to do this, check the system test helpers.
  requestHeaders["User-Agent"] = "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.0 (KHTML, like Gecko) Chrome/6.0.408.1 Safari/534.0"
  http.request("GET", url, headers=requestHeaders)
  resp = http.getresponse()
  body = resp.read()
  print "GET http://%s:%s%s -> %s" % (host, port, url, resp.status)
  http.close()
  return resp, body

def get_primary(url, requestHeaders={}):
  return get(test_fixtures.PRIMARY_HOST, test_fixtures.PRIMARY_PORT, url, requestHeaders)

def get_until(host, port, url, requestHeaders, predicate):
  timeout_seconds = time.time() + 15
  while True:
    response, data = get(host, port, url)
    if predicate(response, data):
      break
    if time.time() > timeout_seconds:
      raise Exception("get_until timed out")

def get_until_primary(url, requestHeaders, predicate):
  return get_until(test_fixtures.PRIMARY_HOST, test_fixtures.PRIMARY_PORT, url, requestHeaders, predicate)


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
