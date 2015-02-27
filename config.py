############################### test args      ################################
NGX_BINARY = "/home/oschaaf/Code/google/ngxps-ttpr/testing/sbin/nginx"
MPS_DIRECTORY = "/home/oschaaf/Code/google/ngxps-ttpr/mod_pagespeed"
PRIMARY_HOST = "localhost"
PRIMARY_PORT = 8050
SECONDARY_HOST = "localhost"
SECONDARY_PORT = 8051
PRIMARY_SERVER = "http://%s:%s" % (PRIMARY_HOST, PRIMARY_PORT)
SECONDARY_SERVER = "http://%s:%s" % (SECONDARY_HOST, SECONDARY_PORT)
CONFIGURATION = ("/home/oschaaf/Code/google/ngxps-ttpr/ngx_pagespeed/test/tmp/"
    "pagespeed_test.conf")
EXAMPLE_ROOT = "/mod_pagespeed_example"
# TODO(oschaaf): CHECK
REWRITTEN_ROOT = "/mod_pagespeed_example"
TEST_ROOT = "/mod_pagespeed_test"
SINGLE_SERVER_INSTANCE = False
BAD_RESOURCE_URL = "/mod_pagespeed/W.bad.pagespeed.cf.hash.css"
DEFAULT_USER_AGENT = ("Mozilla/5.0 (X11; U; Linux x86_64; en-US) "
    "AppleWebKit/534.0 (KHTML, like Gecko) Chrome/6.0.408.1 Safari/534.0")

HTTPS_HOST = ""  # SECONDARY_HOST
HTTPS_EXAMPLE_ROOT = "http://%s/mod_pagespeed_example" % HTTPS_HOST

PROXY_DOMAIN = "%s:%s" % (PRIMARY_HOST, PRIMARY_PORT)
PSA_JS_LIBRARY_URL_PREFIX = "pagespeed_custom_static"
REWRITTEN_TEST_ROOT = TEST_ROOT

LOG_ROOT="/tmp/mod_pagespeed_test.oschaaf/"
