import pytest
from mylib import clean_names

@pytest.mark.parametrize("input_value,expected", [
    ("carrot ", "Carrot"),
    ("LETTUCE", "Lettuce"),
    (" broccoli  ", "Broccoli"),
])
def test_clean_names(input_value, expected):
    assert clean_names(input_value) == expected

