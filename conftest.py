# content of conftest.py
import sys

def pytest_addoption(parser):
  parser.addoption ('--count', default=1, type='int', metavar='count', help='Run each test the specified number of times')

def pytest_generate_tests (metafunc):
    for i in range (metafunc.config.option.count):
        metafunc.addcall()
