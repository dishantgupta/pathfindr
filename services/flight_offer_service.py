import datetime

from flask import make_response, jsonify

from errors.exception import ValidationException, AmadeusException
from integration.amadeus.flight_offers_cache import get_cached_flight_offers
from utils.utils import validate_date


def validate_input_data(payload):

    if not payload.get('origin'):
        raise ValidationException("origin is mandatory")
    origin = str(payload.get('origin')).strip().upper()
    payload['origin'] = origin

    if not origin.isalpha():
        raise ValidationException("origin needs to be alphabetical")
    if len(origin) != 3:
        raise ValidationException("origin should be a 3 letter code")

    if not payload.get('destination'):
        raise ValidationException("destination is mandatory")
    destination = str(payload.get('destination')).strip().upper()
    payload['destination'] = destination

    if not destination.isalpha():
        raise ValidationException("destination needs to be alphabetical")
    if len(destination) != 3:
        raise ValidationException("destination should be a 3 letter code")

    if not payload.get('date'):
        raise ValidationException("date is mandatory")
    date = validate_date(payload.get('date'))
    if not date:
        raise ValidationException("date is invalid")
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    if date < current_datetime:
        raise ValidationException("date is in past; current time: {}".format(current_datetime))

    nocache = payload.get('nocache') or ''
    if str(nocache).lower() == 'true':
        nocache = True
    else:
        nocache = False
    payload['nocache'] = nocache


def get_flights(params):

    try:
        validate_input_data(params)
        resp = get_cached_flight_offers(
            origin_location_code=params['origin'],
            destination_location_code=params['destination'],
            departure_date=params['date'],
            nocache=params.get('nocache')
        )
        response = make_response(jsonify(resp))
        response.status_code = 200
        return response
    except ValidationException as e:
        data = {
            'error': e.ERROR_CODE,
            'error_message': e.message
        }
        response = make_response(jsonify(data))
        response.status_code = 400
        return response
    except AmadeusException as e:
        data = {
            'error': e.ERROR_CODE,
            'error_message': e.message
        }
        response = make_response(jsonify(data))
        response.status_code = 400
        return response

