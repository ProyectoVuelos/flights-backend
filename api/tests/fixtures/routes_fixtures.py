from datetime import datetime
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
    return Flight(
        flight_id=1,
        fr24_id="A1B2C3D4",
        flight="UAL123",
        callsign="UNITED123",
        aircraft_model="Boeing 737",
        aircraft_reg="N123UA",
        departure="LAX",
        arrival="JFK",
        created_at=datetime.now(),
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
