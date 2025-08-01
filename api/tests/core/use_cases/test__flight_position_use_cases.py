from api.core.use_cases.flight_position_use_cases import FlightPositionUseCase


def test_add_positions_to_flight_success(position_port_mock, sample_positions):
    """Test adding flight positions successfully."""
    position_port_mock.add_positions.return_value = True
    use_case = FlightPositionUseCase(position_port=position_port_mock)

    result = use_case.add_positions_to_flight(1, sample_positions)

    position_port_mock.add_positions.assert_called_once_with(1, sample_positions)
    assert result is True


def test_get_positions_for_flight(position_port_mock, sample_positions):
    """Test retrieving positions for a flight."""
    position_port_mock.get_positions_by_flight_id.return_value = sample_positions
    use_case = FlightPositionUseCase(position_port=position_port_mock)

    result = use_case.get_positions_for_flight(1)

    position_port_mock.get_positions_by_flight_id.assert_called_once_with(1)
    assert result == sample_positions
