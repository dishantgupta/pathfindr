from exception import ValidationException
from integration.amadeus.flight_offers_cache import get_cached_flight_offers
from utils import validate_date


def validate_input_data(payload):

    if not payload.get('origin_location_code'):
        raise ValidationException("origin_location_code is mandatory")
    if not payload.get('destination_location_code'):
        raise ValidationException("destination_location_code is mandatory")

    if not payload.get('departure_date'):
        raise ValidationException("departure_date is mandatory")
    date = validate_date(payload.get('departure_date'))
    if not date:
        raise ValidationException("departure_date is invalid")

    adults = payload.get('adults')
    if not adults:
        raise ValidationException("adults must be greater than 0")
    if int(adults) <= 0:
        raise ValidationException("adults must be greater than 0")
    if int(adults) > 9:
        raise ValidationException("adults must be smaller than 10")

    _max = payload.get('max')
    if not _max:
        raise ValidationException("max must be greater than 0")
    if int(_max) <= 0:
        raise ValidationException("max must be greater than 0")
    if int(_max) > 250:
        raise ValidationException("max must be smaller than 250")


def get_flights(params):
    validate_input_data(params)
    resp = get_cached_flight_offers(
        origin_location_code=params['origin_location_code'],
        destination_location_code=params['destination_location_code'],
        departure_date=params['departure_date'],
        adults=int(params['adults']), max=int(params['max']),
        nocache=params.get('nocache') or False
    )
    return resp
