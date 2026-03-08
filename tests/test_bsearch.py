import pytest
from bsearch import BinarySearch


@pytest.fixture
def haystack():
    return [1, 5, 7, 6, 8, 9, 2, 4, 3]


@pytest.fixture
def invalid_haystack():
    return {"as": "me", 1: "b", "2": 3}


@pytest.fixture
def needle():
    return 4


@pytest.fixture
def missing_needle():
    return 111


def test_search_needle(needle, haystack):
    bs = BinarySearch()
    assert bs.search(needle, haystack) == 3


def test_search_not_found(missing_needle, haystack):
    bs = BinarySearch()
    assert bs.search(missing_needle, haystack) is None


def test_search_invalid_haystack(needle, invalid_haystack):
    bs = BinarySearch()
    with pytest.raises((TypeError, AttributeError)):
        bs.search(needle, invalid_haystack)
