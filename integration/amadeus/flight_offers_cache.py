import json

from cache import redis
from integration.amadeus.flight_offers import get_flight_offers

FLIGHT_OFFERS_TTL = 1800


def __get_flight_offers_cache_key(
        origin_location_code: str,
        destination_location_code: str,
        departure_date: str,
        adults: int,
        max: int,
):
    return "amadeus-flight-offers-cache-|{}|{}|{}|{}|{}".format(
        origin_location_code,
        destination_location_code,
        departure_date, adults, max
    )


def __create_flight_offers_cache(params):
    token = get_flight_offers(**params)
    redis.set(
        __get_flight_offers_cache_key(**params),
        json.dumps(token),
        ttl=FLIGHT_OFFERS_TTL
    )


def __get_flight_offers_cache(params):
    token = redis.get(__get_flight_offers_cache_key(**params))
    return token


def get_cached_flight_offers(nocache=False, **params):
    if nocache:
        __create_flight_offers_cache(params)
    resp = __get_flight_offers_cache(params)
    if not resp:
        __create_flight_offers_cache(params)
        resp = __get_flight_offers_cache(params)
    resp = json.loads(resp)
    return resp

