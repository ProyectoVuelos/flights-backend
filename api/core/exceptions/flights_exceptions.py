class FlightNotFoundError(Exception):
    """Raised when a requested flight is not found."""

    pass


class FlightCannotBeAddedError(Exception):
    """Raised when a flight cannot be added."""

    pass
