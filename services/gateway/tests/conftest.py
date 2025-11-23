import pytest


@pytest.fixture
def sample_matrix():
    """Sample matrix for testing"""
    return [[1, 2, 3], [4, 5, 6]]


@pytest.fixture
def sample_data():
    """Sample statistical data for testing"""
    return [1.0, 2.0, 3.0, 4.0, 5.0]
