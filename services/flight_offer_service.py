from integration.amadeus.flight_offers import get_flight_offers


def get_flights():
    resp = get_flight_offers(
        "JFK", "LAX", "2024-12-01", 1, 1
    )
    return resp
