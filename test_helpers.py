from collections import namedtuple
from copy import copy
import errno
import httplib
from pprint import pprint
import re
from socket import error as socket_error
import sys
import time
from time import mktime
import urllib3
from wsgiref.handlers import format_date_time

import config


FetchResult = namedtuple('FetchResult', 'resp body')
http = urllib3.PoolManager()

# TODO(oschaaf): consider removing all these named args and just forward all
# to http.request?
def fetch_url(
    method, url, headers = None, body = None, log = True, timeout = None,
    check = None, proxy = None):
    assert url.startswith("http")

    headers = {} if headers is None else copy(headers)
    timeout = urllib3.Timeout(total=10.0) if timeout is None else timeout

    if not "User-Agent" in headers:
        headers["User-Agent"] = config.DEFAULT_USER_AGENT

    if proxy:
        if url.find(proxy) == 0:
            # Get the to-be-proxied host on the first request line
            url = url.replace(proxy, headers["Host"], 1)
        pm = urllib3.ProxyManager(proxy)
        resp = pm.request(
            method, url, headers = headers, timeout = timeout, retries = False)
    else:
        resp = http.request(
            method, url, headers = headers, timeout = timeout, retries = False)
    body = resp.data

    if log:
        # TODO(oschaaf): log to a file/test
        print "fetch_url: %s %s: %s" % (method, url, resp.status)
        print "req. headers VVVVVVVV"
        pprint(headers)
        print "^^^^^^^^^^^^^^^^^^^^^"
        print "res. headers VVVVVVVV"
        pprint(resp.getheaders())
        print "^^^^^^^^^^^^^^^^^^^^^"
    if not check is None:
        assert check(resp, body)
    return FetchResult(resp, body)

# Perform http requests until the predicate evaluates the response to True.
# Current time limit is 5 seconds, 0.1 second sleep will be done between
# subsequent tries.
# Any named arguments will be passed on to fetch_url.
def fetch_until(method, url, predicate, *args, **kwargs):
    print "fetch_until(): %s %s" % (method, url)
    timeout_seconds = time.time() + 5
    ok = True
    while True:
        response, data = fetch_url(method, url, *args, **kwargs)

        if ok:
            if predicate(response, data):
                return FetchResult(response, data)
        else:
            assert predicate(response, data)
            return FetchResult(response, data)

        time.sleep(0.1)
        if time.time() > timeout_seconds:
            # We try one more time when time us up, so we can log some info.
            if not ok:
                assert not "Timeout waiting for predicate"
            ok = False

# Same as fetch_url, but defaulting to a GET request
def get_url(url, *args, **kwargs):
    return fetch_url("GET", url, *args, **kwargs)

# Same as fetch_url, but defaulting to a GET request on the primary domain
# Instead of a url, pass in a path (e.g.: /mod_pagespeed_example)
def get_primary(path, *args, **kwargs):
    assert not path.startswith("http")
    url = "%s%s" % (config.PRIMARY_SERVER, path)
    return get_url(url, *args, **kwargs)

# fetch_until, using GET requests on the primary domain.
# Specify a path instead of a full url
def get_until_primary(path, predicate, *args, **kwargs):
    assert not path.startswith("http")
    url = "%s%s" % (config.PRIMARY_SERVER, path)
    return get_url_until(url, predicate, *args, **kwargs)

# fetch_until, using GET requests.
def get_url_until(url, predicate, *args, **kwargs):
    return fetch_until("GET", url, predicate, *args, **kwargs)

# Transform the passed in date into a formatted string usable in
# http Date: headers
def http_date(d):
    stamp = mktime(d.timetuple())
    return format_date_time(stamp)

# TODO(check resp.status == 200 as well?)
def CheckSubstringCountEquals(string_to_search, count):
    return lambda _resp, body: body.count(string_to_search) == count

# TODO(check resp.status == 200 as well?)
# TODO(oschaaf): upon using, something weird seems to happen, possible
# triggering a bug in py.tests's introspection for explaining the assert
# failure.
def CheckPatternCountEquals(pattern, count):
    return lambda _resp, body: re.findall(pattern, "body") == count

