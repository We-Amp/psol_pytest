import re

import pytest

import config
import test_helpers as helpers

skip = "not config.SECONDARY_HOST"
combined_css = ".yellow{background-color:#ff0}"
url_regex = r'http:\/\/[^ ]+css\.pagespeed[^ ]+\.css'
url_path = "/mod_pagespeed_test/unauthorized/inline_css.html"
opts  = "?PageSpeedFilters=rewrite_images,rewrite_css"
page_url = "%s%s%s" % (config.SECONDARY_SERVER, url_path, opts)


@pytest.mark.skipif(skip)
class TestSignedUrls:
    def get_resource_url(self, headers):
        resp, body = helpers.get_url_until(page_url,
          lambda resp, body: body.count("all_styles.css.pagespeed.cf") == 1,
          headers = headers, proxy = config.SECONDARY_SERVER)
        match = re.search(url_regex, body, re.MULTILINE)
        assert match
        assert resp.status == 200
        resource_url = match.group(0)
        return resource_url

    # Signed Urls : Correct URL signature is passed
    def test_signature_is_passed(self):
        headers = {"Host": "signed-urls.example.com"}
        resource_url = self.get_resource_url(headers)
        helpers.get_url_until(resource_url,
            lambda resp, body: body.count(combined_css) == 1,
            headers = headers, proxy = config.SECONDARY_SERVER)

    def test_incorrect_url_signature_is_passed(self):
        headers = {"Host": "signed-urls.example.com"}
        resource_url = self.get_resource_url(headers)
        # Replace valid signature with an invalid one
        invalid_url = "%sAAAAAAAAAA.css" % resource_url[:-14]
        resp, body = helpers.get_url(invalid_url, headers = headers,
            proxy = config.SECONDARY_SERVER)
        assert resp.status == 404 or resp.status == 403

    def test_no_signature_is_passed(self):
        headers = {"Host": "signed-urls.example.com"}
        resource_url = self.get_resource_url(headers)
        # Remove signature
        invalid_url = "%s.css" % resource_url[:-14]
        resp, body = helpers.get_url(invalid_url, headers = headers,
            proxy = config.SECONDARY_SERVER)
        assert resp.status == 404 or resp.status == 403

    def test_ignored_signature_correct_url_signature_is_passed(self):
        headers = {"Host": "signed-urls-transition.example.com"}
        resource_url = self.get_resource_url(headers)
        helpers.get_url_until(resource_url,
            lambda resp, body: body.count(combined_css) == 1,
            headers = headers, proxy = config.SECONDARY_SERVER)

    def test_ignored_signature_incorrect_url_signature_is_passed(self):
        headers = {"Host": "signed-urls-transition.example.com"}
        resource_url = self.get_resource_url(headers)
        invalid_url = "%sAAAAAAAAAA.css" % resource_url[:-14]
        helpers.get_url_until(invalid_url,
            lambda resp, body: body.count(combined_css) == 1,
            headers = headers, proxy = config.SECONDARY_SERVER)

    def test_ignored_signature_no_signature_is_passed(self):
        headers = {"Host": "signed-urls-transition.example.com"}
        resource_url = self.get_resource_url(headers)
        invalid_url = "%s.css" % resource_url[:-14]

        helpers.get_url_until(invalid_url,
            lambda resp, body: body.count(combined_css) == 1,
            headers = headers, proxy = config.SECONDARY_SERVER)

    def test_unsigned_urls_ignored_signatures_bad_signature_is_passed(self):
        headers = {"Host": "unsigned-urls-transition.example.com"}
        resource_url = self.get_resource_url(headers)
        invalid_url = resource_url.replace("Cxc4pzojlP", "UH8L-zY4b4AAAAAAAAAA")
        helpers.get_url_until(invalid_url,
            lambda resp, body: body.count(combined_css) == 1,
            headers = headers, proxy = config.SECONDARY_SERVER)

    def test_unsigned_urls_ignored_signatures_no_signature_is_passed(self):
        headers = {"Host": "unsigned-urls-transition.example.com"}
        resource_url = self.get_resource_url(headers)
        invalid_url = resource_url.replace("Cxc4pzojlP", "UH8L-zY4b4")
        helpers.get_url_until(invalid_url,
            lambda resp, body: body.count(combined_css) == 1,
            headers = headers, proxy = config.SECONDARY_SERVER)
