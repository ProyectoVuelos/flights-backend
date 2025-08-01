from datetime import datetime
from unittest.mock import MagicMock

import pytest

from api.core.domain.flight import Flight
from api.core.domain.flight_position import FlightPosition
from api.core.exceptions.flights_exceptions import FlightNotFoundError
from api.core.ports.flight_port import FlightPort
from api.core.ports.flight_position_port import FlightPositionPort
from api.core.use_cases.flight_position_use_cases import FlightPositionUseCase
from api.core.use_cases.flight_use_cases import FlightUseCase


@pytest.fixture
def flight_port_mock():
    """Fixture to create a mock FlightPort."""
    return MagicMock(spec=FlightPort)


@pytest.fixture
def position_port_mock():
    """Fixture to create a mock FlightPositionPort."""
    return MagicMock(spec=FlightPositionPort)


@pytest.fixture
def sample_flight():
    """Fixture to create a sample Flight object."""
    return Flight(
        flight_id=1,
        fr24_id="A1B2C3D4",
        flight="UAL123",
        callsign="UNITED123",
        created_at=datetime.now(),
    )


@pytest.fixture
def sample_positions():
    """Fixture to create a list of sample FlightPosition objects."""
    return [
        FlightPosition(
            flight_id=1, timestamp=datetime.now(), latitude=10.0, longitude=20.0
        ),
        FlightPosition(
            flight_id=1, timestamp=datetime.now(), latitude=11.0, longitude=21.0
        ),
    ]
