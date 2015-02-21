# psol_pytest
Porting Google PSOL bash system tests to python

E.g:

```
oschaaf@ubuntu:~/Code/google/psol_pytest⟫ py.test -v -k extend
============================================================================== test session starts ===============================================================================
platform linux2 -- Python 2.7.6 -- py-1.4.26 -- pytest-2.6.4 -- /usr/bin/python
plugins: xdist
collected 26 items 

system/test_extend_cache.py::test_extend_cache_images_rewrites_an_image_tag[0] PASSED
system/test_extend_cache.py::test_attempt_to_fetch_cache_extended_image_without_hash_should_404[0] PASSED
system/test_extend_cache.py::test_cache_extended_image_should_respond_304_to_an_if_modified_since[0] PASSED
system/test_extend_cache.py::test_legacy_format_urls_should_still_work[0] PASSED

======================================================================= 22 tests deselected by '-kextend' ========================================================================
==================================================================== 4 passed, 22 deselected in 1.52 seconds =====================================================================
oschaaf@ubuntu:~/Code/google/psol_pytest⟫ 
```
