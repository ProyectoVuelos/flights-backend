from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.core.domain.flight import Flight
from api.core.domain.flight_position import FlightPosition
from api.core.use_cases.flight_position_use_cases import FlightPositionUseCase
from api.core.use_cases.flight_use_cases import FlightUseCase
from api.index import app


@pytest.fixture
def client():
    """Fixture to create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_flight_service():
    """Fixture to create a mock FlightUseCase instance."""
    return MagicMock(spec=FlightUseCase)


@pytest.fixture
def mock_position_service():
    """Fixture to create a mock FlightPositionUseCase instance."""
    return MagicMock(spec=FlightPositionUseCase)


@pytest.fixture
def sample_flight():
    """Fixture to create a sample Flight object for testing."""
    now = datetime.now(timezone.utc)
    return Flight(
        flight_id=1,
        fr24_id="3b9c0a1f",
        flight="UA123",
        callsign="UAL123",
        
        aircraft_model="B738",
        aircraft_reg="N123UA",
        
        departure_icao="KLAX",
        arrival_icao="KJFK",
        departure_time_utc=now - timedelta(hours=5),
        arrival_time_utc=now,
        flight_duration_s=18000,
        distance_calculated_km=3982.5,
        great_circle_distance_km=3979.0,

        duration_takeoff_s=180,
        duration_climb_s=1500,
        duration_cruise_s=14820,
        duration_descent_s=1200,
        duration_landing_s=300,

        fuel_takeoff_kg=200.0,
        fuel_climb_kg=1200.0,
        fuel_cruise_kg=8200.0,
        fuel_descent_kg=500.0,
        fuel_landing_kg=100.0,
        
        co2_takeoff_kg=632.0,
        co2_climb_kg=3792.0,
        co2_cruise_kg=25912.0,
        co2_descent_kg=1580.0,
        co2_landing_kg=316.0,
        co2_total_kg=32232.0,
        co2_per_passenger_kg=179.07,
        
        created_at=now,
        last_updated=now
    )


@pytest.fixture
def sample_positions():
    """Fixture to create a list of sample FlightPosition objects."""
    return [
        FlightPosition(
            flight_id=1,
            position_id=1,
            timestamp=datetime.now(),
            latitude=34.0522,
            longitude=-118.2437,
        ),
        FlightPosition(
            flight_id=1,
            position_id=2,
            timestamp=datetime.now(),
            latitude=40.7128,
            longitude=-74.0060,
        ),
    ]
