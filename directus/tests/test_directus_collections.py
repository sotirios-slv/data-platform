import os
import sys

import pytest

# Set directory to parent level so that function can be imported for test
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from directus_collections import get_collections


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("include_default_collections=True", list),
        ("include_default_collections=False", list),
    ],
)
def test_get_collections(test_input, expected):
    assert isinstance(get_collections(test_input), expected)
