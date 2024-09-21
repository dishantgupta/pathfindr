import logging
import traceback

from flask import make_response, jsonify

from errors.exception import ValidationException, AmadeusException
from integration.amadeus.flight_offers_cache import get_cached_flight_offers
from services.flight_offer_validator import validate_input_data


logger = logging.getLogger(__name__)


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
    except Exception as e:
        trcbk = traceback.format_exc()
        logger.error("UNEXPECTED ERROR: flight_offers: params: {}, error: {}".format(params, trcbk))
        data = {
            'error': "UNEXPECTED",
            'error_message': str(e),
            'error_stacktrace': trcbk
        }
        response = make_response(jsonify(data))
        response.status_code = 500
        return response
