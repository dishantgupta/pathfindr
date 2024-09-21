from flask import make_response, jsonify

from errors.exception import ValidationException, AmadeusException
from integration.amadeus.flight_offers_cache import get_cached_flight_offers
from utils.utils import validate_date


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

    try:
        resp = get_cached_flight_offers(
            origin_location_code=params['origin'],
            destination_location_code=params['destination'],
            departure_date=params['date'],
            nocache=params.get('nocache')
        )
    except AmadeusException as e:
        data = {
            'error': e.ERROR_CODE,
            'error_message': e.message
        }
        response = make_response(jsonify(data))
        response.status_code = 400
        return response

    return resp
