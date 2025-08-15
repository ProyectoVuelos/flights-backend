import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

class MockResponse:
    def __init__(self, data):
        self.data = data

from api.adapters.repositories.supabase.flight_repository import SupabaseFlightRepository
from api.core.domain.flight import Flight


@pytest.fixture
def sample_flight_dict():
    """
    Fixture que provee un diccionario de vuelo completo, simulando una respuesta de la base de datos.
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    return {
        "flight_id": 1,
        "fr24_id": "3b9c0a1f",
        "flight": "UA123",
        "callsign": "UAL123",
        "aircraft_model": "B738",
        "aircraft_reg": "N123UA",
        "departure_icao": "KLAX",
        "arrival_icao": "KJFK",
        "departure_time_utc": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat(),
        "arrival_time_utc": now_iso,
        "flight_duration_s": 18000,
        "distance_calculated_km": 3982.5,
        "great_circle_distance_km": 3979.0,
        "duration_takeoff_s": 180,
        "duration_climb_s": 1500,
        "duration_cruise_s": 14820,
        "duration_descent_s": 1200,
        "duration_landing_s": 300,
        "fuel_takeoff_kg": 200.0,
        "fuel_climb_kg": 1200.0,
        "fuel_cruise_kg": 8200.0,
        "fuel_descent_kg": 500.0,
        "fuel_landing_kg": 100.0,
        "co2_takeoff_kg": 632.0,
        "co2_climb_kg": 3792.0,
        "co2_cruise_kg": 25912.0,
        "co2_descent_kg": 1580.0,
        "co2_landing_kg": 316.0,
        "co2_total_kg": 32232.0,
        "co2_per_passenger_kg": 179.07,
        "created_at": now_iso,
        "last_updated": now_iso,
    }


@patch("api.adapters.repositories.supabase.flight_repository.create_client")
def test_add_flight_success(mock_create_client, sample_flight_dict):
    """Test que el repositorio llama a Supabase y devuelve un objeto Flight al añadir."""
    mock_create_client.return_value.table.return_value.insert.return_value.execute.return_value = MockResponse(
        data=[sample_flight_dict]
    )
    repository = SupabaseFlightRepository()    
    new_flight = Flight(fr24_id=sample_flight_dict["fr24_id"], flight=sample_flight_dict["flight"])
    
    result = repository.add(new_flight)

    assert isinstance(result, Flight)
    assert result.fr24_id == sample_flight_dict["fr24_id"]
    assert result.flight_id == sample_flight_dict["flight_id"]


@patch("api.adapters.repositories.supabase.flight_repository.create_client")
def test_get_by_fr24_id_found(mock_create_client, sample_flight_dict):
    """Test que al obtener por FR24 ID se devuelve el objeto correcto."""
    mock_create_client.return_value.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MockResponse(
        data=sample_flight_dict
    )
    repository = SupabaseFlightRepository()
    
    result = repository.get_by_fr24_id("3b9c0a1f")

    assert isinstance(result, Flight)
    assert result.fr24_id == sample_flight_dict["fr24_id"]
    assert result.flight_id == sample_flight_dict["flight_id"]
    assert result.departure_icao == "KLAX"


@patch("api.adapters.repositories.supabase.flight_repository.create_client")
def test_get_by_fr24_id_not_found(mock_create_client):
    """Test que devuelve None si no se encuentra un vuelo por FR24 ID."""
    mock_create_client.return_value.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = MockResponse(
        data=None
    )
    repository = SupabaseFlightRepository()
    
    result = repository.get_by_fr24_id("NONEXISTENT")

    assert result is None


@patch("api.adapters.repositories.supabase.flight_repository.create_client")
def test_find_all(mock_create_client, sample_flight_dict):
    """Test que find_all devuelve una lista de objetos Flight."""
    mock_create_client.return_value.table.return_value.select.return_value.range.return_value.execute.return_value = MockResponse(
        data=[sample_flight_dict, sample_flight_dict]
    )
    repository = SupabaseFlightRepository()
    
    results = repository.find_all(limit=2, offset=0)

    assert len(results) == 2
    assert isinstance(results[0], Flight)
    assert results[1].fr24_id == sample_flight_dict["fr24_id"]
