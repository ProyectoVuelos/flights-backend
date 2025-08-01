from datetime import datetime
from unittest.mock import patch

from postgrest import APIResponse

from api.adapters.repositories.supabase.flight_position_repository import \
    SupabaseFlightPositionRepository
from api.adapters.repositories.supabase.flight_repository import \
    SupabaseFlightRepository
from api.core.domain.flight import Flight
from api.core.domain.flight_position import FlightPosition
from api.tests.fixtures.supabase_fixtures import MockResponse


@patch("api.adapters.repositories.supabase.flight_repository.create_client")
def test_add_flight_success(mock_create_client):
    """Test that the repository correctly calls Supabase and returns a Flight object."""
    mock_create_client.return_value.table.return_value.insert.return_value.execute.return_value = MockResponse(
        data=[
            {
                "flight_id": 1,
                "fr24_id": "TEST1234",
                "flight": "MOCK123",
                "created_at": datetime.now().isoformat(),
            }
        ]
    )

    repository = SupabaseFlightRepository()

    new_flight = Flight(fr24_id="TEST1234", flight="MOCK123")
    result = repository.add(new_flight)

    assert isinstance(result, Flight)
    assert result.fr24_id == "TEST1234"
    assert result.flight_id == 1


@patch("api.adapters.repositories.supabase.flight_repository.create_client")
def test_get_by_fr24_id_found(mock_create_client):
    """Test retrieving a flight by FR24 ID returns the correct object."""
    mock_create_client.return_value.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MockResponse(
        data={
            "flight_id": 1,
            "fr24_id": "TEST1234",
            "flight": "MOCK123",
            "created_at": datetime.now().isoformat(),
        }
    )

    repository = SupabaseFlightRepository()
    result = repository.get_by_fr24_id("TEST1234")

    assert isinstance(result, Flight)
    assert result.fr24_id == "TEST1234"
    assert result.flight_id == 1


@patch("api.adapters.repositories.supabase.flight_repository.create_client")
def test_get_by_fr24_id_not_found(mock_create_client):
    """Test retrieving a non-existent flight by FR24 ID returns None."""
    mock_create_client.return_value.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MockResponse(
        data=None
    )

    repository = SupabaseFlightRepository()
    result = repository.get_by_fr24_id("NONEXISTENT")

    assert result is None


@patch("api.adapters.repositories.supabase.flight_repository.create_client")
def test_get_all_flights(mock_create_client):
    """Test retrieving all flights returns a list of Flight objects."""
    mock_create_client.return_value.table.return_value.select.return_value.execute.return_value = APIResponse(
        data=[
            {
                "flight_id": 1,
                "fr24_id": "TEST1",
                "created_at": datetime.now().isoformat(),
            },
            {
                "flight_id": 2,
                "fr24_id": "TEST2",
                "created_at": datetime.now().isoformat(),
            },
        ],
        count=None,
    )
    repository = SupabaseFlightRepository()
    results = repository.find_all()

    assert len(results) == 2
    assert isinstance(results[0], Flight)


@patch("api.adapters.repositories.supabase.flight_repository.create_client")
def test_delete_positions_by_flight_id(mock_create_client):
    """Test deleting positions by flight ID returns True on success."""
    mock_create_client.return_value.table.return_value.delete.return_value.eq.return_value.execute.return_value = APIResponse(
        data=[], count=None
    )
    repository = SupabaseFlightPositionRepository()
    result = repository.delete_positions_by_flight_id(1)
    assert result is True
