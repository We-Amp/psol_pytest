from collections import namedtuple
from copy import copy
import itertools
import re
from socket import error as socket_error
import time
import urllib3
from urlparse import urljoin
from wsgiref.handlers import format_date_time

import config
from config import log

FetchResult = namedtuple('FetchResult', 'resp body')
fetch_count = itertools.count()

def patternCountEquals(self, pattern, count):
    return len(re.findall(pattern, self.body)) == count

def stringCountEquals(self, substring, count):
    return self.body.count(substring) == count


# Wrapper around the fetch generator, providing convenience methods like
# waitFor()
class FetchUntil:
    def __init__(self, url, *args, **kwargs):
        self.it = fetch_generator(url, *args, **kwargs)

    def __iter__(self):
        return self

    def next(self):
        return self.it.next()

    # Perform http requests until the predicate evaluates the response to True.
    # Current time limit is 5 seconds, 0.1 second sleep will be done between
    # subsequent tries.
    # Any named arguments will be passed on to fetch_url.
    def waitFor(self, predicate, *predicate_args):
        res = self.next()
        while True:
            if predicate(res, *predicate_args):
                return res, True
            try:
                res = self.next()
            except StopIteration:
                break

        return res, False

# Relative url will be absolutified to the first match of:
# 1. The host header
# 2. The given proxy
# 3. The primary test host
def fetch(
    url, headers = None, timeout = None, proxy = "",
    method = "GET", allow_error_responses = False):
    mycount = fetch_count.next()
    headers = {} if headers is None else copy(headers)
    timeout = urllib3.Timeout(total=10.0) if timeout is None else timeout
    if not "User-Agent" in headers:
        headers["User-Agent"] = config.DEFAULT_USER_AGENT


    #if proxy:
    #    assert headers["Host"]

    # If a relative path was specified, absolutify it assuming this is a request
    # for the primary test host.
    # TODO(oschaaf): clean up host handling mess
    if not url.startswith("http"):
        if "Host" in headers:
            url = "http://%s%s" % (headers["Host"], url)
        else:
            if proxy:
                url = "%s%s" % (proxy, url)
            else:
                url = "%s%s" % (config.PRIMARY_SERVER, url)

    # Helps cross referencing between this and server log
    headers["PSOL-Fetch-Id"] = mycount
    fetch_method = None
    log.debug("[%d:] fetch_url %s %s: %s" % (mycount, method, url, headers))
    try:
        if proxy:
            fetch_method = urllib3.ProxyManager(proxy).request
        else:
            fetch_method = urllib3.PoolManager().request

        resp = fetch_method(method, url, headers = headers, timeout = timeout,
            retries = False, redirect = False)
    except:
        log.debug("[%d]: fetch_url excepted", mycount)
        raise
    body = resp.data

    log.debug("[%d]: fetch_url %s %s\n>>>>>>>>>>\n%s<<<<<<<<<<<<<" %
        (mycount, resp.status, resp.getheaders(), body))

    if not allow_error_responses:
        assert resp.status < 400, resp.status

    return FetchResult(resp, body)

# Yields fetches for a fixed period, passing on args/kwargs to fetch.
def fetch_generator(url, *args, **kwargs):
    # __tracebackhide__ = True
    timeout_seconds = time.time() + 5
    ok = True
    while ok:
        res = fetch(url, *args, **kwargs)
        yield res
        ok = time.time() < timeout_seconds
        if ok:
            time.sleep(0.2)
    log.debug("Fetch generator timed out")


# Transform the passed in date into a formatted string usable in
# http Date: headers
def http_date(d):
    stamp = time.mktime(d.timetuple())
    return format_date_time(stamp)

def absolutify_url(base_url, relative_url):
    return urljoin(base_url, relative_url)

