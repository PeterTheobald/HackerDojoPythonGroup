# Python testing with doctest

unittest - built into Python
pytest - newer improved testing
doctest - simple testing integrated with internal docs (comments)

doctest isn't meant to replace pytest. It's meant to allow you to
add simple internal testing to your code, and to keep your docs
correct. Docs often go out of sync with the actual code changes.
Doctest makes your docs into live tests.

What does pytest give you that doctest doesn't?
- parameterization (testing many different example inputs)
- fixtures (setup and cleanup functions)
- mocking (replacing dependencies like database calls or network calls with fake results)
- coverage (pytest-cov can report how much of your code is being tested)

Use doctest for core modules and reusable logic where the functions
are small and mostly pure (no side effects)
Use pytest for actual test cases, edge conditions, performance guards, etc

## USAGE

Doctest is really easy. Just include Python REPL commands and expected output
in the docstring.
This serves both as a test and as an example for documentation.

```
def clean_names(name):
    """
    Removes trailing whitespace and capitalizes the name.

    >>> clean_names("  peter  ")
    'Peter'
    >>> clean_names("JOSHUA")
    'Joshua'
    """
    return name.strip().capitalize()
```

## vs. Pytest

Now here's how Pytest parameterization can give you better coverage:

mylib_test.py
```
import pytest
from mylib import clean_names

@pytest.mark.parametrize("input_value,expected", [
    ("carrot ", "Carrot"),
    ("LETTUCE", "Lettuce"),
    (" broccoli  ", "Broccoli"),
])
def test_clean_names(input_value, expected):
    assert clean_names(input_value) == expected
```

Put pytests in the folder tests/ and put doctests inline in your code.

## How to run doctests manually

`uv run python -m doctest -v mylib.py`
(or if you're not using uv, just `python -m doctest -v mylib.py`)

## or add a test runner to your main:

```
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True) # Set verbose=True for detailed output
```

run:
`uv run mylib.py`

## or integrate Pytest and Doctest

Run all doctests found in Python code *AND* all pytest \_test files:

`pytest --doctest-modules`

## or configure pytest to always run doctests:

pyproject.toml:
```
[tool.pytest.ini_options]
addopts = "--doctest-modules"
```

