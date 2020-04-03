import random

import pytest

from sandberg.utils import key_finder

def test_key_finder():
    random.seed(7)
    key = key_finder()
    assert key == "F"
