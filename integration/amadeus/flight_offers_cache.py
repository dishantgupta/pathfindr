import json
import logging

from cache import redis
from config.env import get_env_variable
from integration.amadeus.flight_offers import get_flight_offers


logger = logging.getLogger(__name__)


def __get_flight_offers_cache_ttl():
    return int(get_env_variable("AMADEUS_FLIGHT_OFFERS_CACHE_TTL"))


def __get_flight_offers_cache_key(
        origin_location_code: str,
        destination_location_code: str,
        departure_date: str
):
    return "amadeus-flight-offers-cache-|{}|{}|{}|".format(
        origin_location_code,
        destination_location_code,
        departure_date
    )


def __create_flight_offers_cache(params):
    amadeus_flight_offers_resp = get_flight_offers(**params)
    flight_offers_resp = get_cheapest_flight(amadeus_flight_offers_resp)
    redis.set(
        __get_flight_offers_cache_key(**params),
        json.dumps(flight_offers_resp),
        ttl=__get_flight_offers_cache_ttl()
    )


def __get_flight_offers_cache(params):
    token = redis.get(__get_flight_offers_cache_key(**params))
    return token


def get_cached_flight_offers(nocache=False, **params):
    if nocache:
        logger.debug("AMADEUS flight offers explicit cache refresh using nocache flag")
        __create_flight_offers_cache(params)
    resp = __get_flight_offers_cache(params)
    if not resp:
        logger.debug("AMADEUS flight offers not found in cache for params: {}".format(params))
        __create_flight_offers_cache(params)
        logger.debug("AMADEUS flight offers not found in cache; cache created")
        resp = __get_flight_offers_cache(params)
    resp = json.loads(resp)
    return resp


def get_cheapest_flight(resp):
    _data = resp.get('data', [{}])
    minimum_price_flight = {}
    minimum_price_flight_price = None

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
                        flight_data['data']['price'] = data['price']['base'] + ' ' + data['price']['currency']

                        if minimum_price_flight_price is None:
                            minimum_price_flight_price = data['price']['base']
                            minimum_price_flight = flight_data
                        else:
                            if data['price']['base'] < minimum_price_flight_price:
                                minimum_price_flight_price = data['price']['base']
                                minimum_price_flight = flight_data
    return minimum_price_flight
