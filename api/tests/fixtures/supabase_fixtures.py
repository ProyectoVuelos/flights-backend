from unittest.mock import MagicMock

import pytest


class MockResponse:
    def __init__(self, data=None):
        self.data = data if data is not None else []


class MockTable:
    def __init__(self, data=None):
        self._data = data if data is not None else []

    def insert(self, data):
        return self

    def select(self, columns):
        return self

    def eq(self, column, value):
        return self

    def single(self):
        return self

    def execute(self):
        return MockResponse(self._data)


@pytest.fixture
def supabase_client_mock():
    """Fixture to create a mock Supabase client."""
    client = MagicMock()
    client.table.return_value = MockTable()
    return client
