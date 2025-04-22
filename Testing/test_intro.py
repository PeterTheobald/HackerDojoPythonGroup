import os


def test_addition():
  assert 1 + 1 == 2


def test_subtraction():
  assert 2 - 1 == 1


def myfunc(i):
  return i * 2


def test_myfunc():
  assert myfunc(1) == 2


#######################

import pytest


# activated by using fixture fn as an argument
@pytest.fixture
def sample_data():
  return [1, 2, 3, 4, 5]


def test_sum(sample_data):
  assert sum(sample_data) == 15


@pytest.fixture
def temporary_file():
  # runs before each test:
  with open("temp_file.txt", "w") as f:
    f.write("hello")
  yield "temp_file.txt"
  # runs after each test:
  os.remove("temp_file.txt")


# run for every test, even if setup_env isn't referenced
@pytest.fixture(autouse=True)
def setup_env():
  os.environ["API_KEY"] = "123xyz"
  yield
  del os.environ["API_KEY"]


#######################
# marks


@pytest.mark.parametrize("num, expected", [(1, 2), (2, 3), (3, 4)])
def test_increment(num, expected):
  assert num + 1 == expected


# this will test x,y=(0,2) (0,3) (1,2) (1,3)
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_multiply(x, y):
  assert x * y == x * y  # Simplistic test


###############################################

import sys


@pytest.mark.skip(reason="This feature has not been implemented yet")
def test_future_feature():
  pass


@pytest.mark.skipif(sys.version_info < (3, 10),
                    reason="Requires Python 3.10 or higher")
def test_feature_for_new_python():
  pass


@pytest.mark.xfail(reason="Known parser issue in version 1.2")
def test_parser():
  assert parse_data("input") == "expected output"

@pytest.mark.slow_test()
def test_slowest_ever():
  pass
  
# custom markers like 'slow_tests', 'critical_tests' or 'network_tests' etc
# run with `pytest -m critical` or `pytest -m "not slow_tests"`

# mocking

from unittest.mock import Mock


def function_being_tested(some_object):
  return some_object.some_method(42)


@pytest.fixture
def mock_object():
  mock = Mock()
  mock.some_method.return_value = 'Mock response'
  return mock


def test_function_with_fixture(mock_object):
  # The mock_object fixture is automatically passed into the test function
  result = function_being_tested(mock_object)
  assert result == 'Mock response'


# plugins like parallel

