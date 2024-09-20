from exception import ValidationException
from integration.amadeus.flight_offers_cache import get_cached_flight_offers
from utils import validate_date


def validate_input_data(payload):

    if not payload.get('origin'):
        raise ValidationException("origin is mandatory")
    if not payload.get('destination'):
        raise ValidationException("destination is mandatory")

    if not payload.get('date'):
        raise ValidationException("date is mandatory")
    date = validate_date(payload.get('date'))
    if not date:
        raise ValidationException("date is invalid")

    nocache = payload.get('nocache') or ''
    if str(nocache).lower() == 'true':
        nocache = True
    else:
        nocache = False
    payload['nocache'] = nocache


def get_flights(params):
    validate_input_data(params)

    resp = get_cached_flight_offers(
        origin_location_code=params['origin'],
        destination_location_code=params['destination'],
        departure_date=params['date'],
        nocache=params.get('nocache')
    )
    return format_response(resp)


def format_response(resp):
    flight_data_list = []
    _data = resp.get('data', [{}])
    if _data:
        for data in _data:
            flight_data = {"data": {}}
            if data:
                itineraries = data.get('itineraries') or []
                if itineraries:
                    itinerary = itineraries[0]
                    segments = itinerary.get('segments') or []
                    if segments:
                        segment = segments[0]
                        flight_data['data']['origin'] = segment['departure']['iataCode']
                        flight_data['data']['destination'] = segment['arrival']['iataCode']
                        flight_data['data']['departure_date'] = segment['departure']['at']
                        flight_data['data']['price'] = data['price']['base'] + data['price']['currency']
                        flight_data_list.append(flight_data)
    return flight_data_list