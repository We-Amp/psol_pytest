import httplib
import test_fixtures
import time
import sys

def get(host, port, url, requestHeaders = {}):
  http = httplib.HTTPConnection(host, port, timeout=30)
  http.connect()
  http.request("GET", url, headers=requestHeaders)
  response = http.getresponse()
  data = response.read()
  http.close()
  return response, data

def get_primary(url, requestHeaders={}):
  return get(test_fixtures.PRIMARY_HOST, test_fixtures.PRIMARY_PORT, url, requestHeaders)

def get_until(host, port, url, requestHeaders, predicate):
  timeout_seconds = time.time() + 30
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


