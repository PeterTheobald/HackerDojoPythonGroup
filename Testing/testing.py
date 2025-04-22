# Unit tests
# Integration tests

# pip install pytest
#
# name files 
# name functions test_<func>()
#
# run tests with `pytest`
#

# test coverage
# TDD test driven development (Red/Green/Refactor)
# CI/CD continuous integration
#    github actions
#
"""
# keep dependencies isolated:
def messy_func():
  d = database stuff
  data = read from database
  do lots of calculations on data
  write to database( data)

def clean_func():
  d = database stuff
  data = read from database
  data = do_calculations(data)
  write to database( data)

# now you can write tests of do_calculations()
"""

################
# parallel tests

# pip install pytest-xdist
# pytest -n 4 (use 4 cores)

# run on 4 different machines across the network
# pytest --dist=loadscope --tx ssh=//user@hostname//python=python3 -n 4


try:
  my_func()
except:
  handle error
