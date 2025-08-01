import pytest

from api.core.exceptions.flights_exceptions import FlightNotFoundError
from api.core.use_cases.flight_use_cases import FlightUseCase


def test_add_new_flight(flight_port_mock, sample_flight):
    """Test that adding a new flight works and returns the new flight object."""
    flight_port_mock.add.return_value = sample_flight
    use_case = FlightUseCase(flight_port=flight_port_mock)

    result = use_case.add_new_flight(sample_flight)

    flight_port_mock.add.assert_called_once_with(sample_flight)
    assert result == sample_flight


def test_get_flight_by_id_success(flight_port_mock, sample_flight):
    """Test retrieving a flight by ID successfully."""
    flight_port_mock.get_by_id.return_value = sample_flight
    use_case = FlightUseCase(flight_port=flight_port_mock)

    result = use_case.get_flight_by_id(1)

    flight_port_mock.get_by_id.assert_called_once_with(1)
    assert result == sample_flight


def test_get_flight_by_id_not_found(flight_port_mock):
    """Test that getting a non-existent flight raises an exception."""
    flight_port_mock.get_by_id.return_value = None
    use_case = FlightUseCase(flight_port=flight_port_mock)

    with pytest.raises(FlightNotFoundError):
        use_case.get_flight_by_id(999)


def test_get_all_flights(flight_port_mock, sample_flight):
    """Test retrieving all flights."""
    flight_port_mock.find_all.return_value = [sample_flight]
    use_case = FlightUseCase(flight_port=flight_port_mock)

    result = use_case.get_all_flights()

    flight_port_mock.find_all.assert_called_once()
    assert result == [sample_flight]
