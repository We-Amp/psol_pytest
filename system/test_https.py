import re

import config
import test_helpers as helpers

# TODO(oschaaf): might not even be close to OK. revisit this laterself.


def test_simple_test_that_https_is_working():
    if config.HTTPS_HOST:
        assert False
