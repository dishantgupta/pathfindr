import json

from cache import redis
from config.env import get_env_variable
from integration.amadeus.flight_offers import get_flight_offers


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
    token = get_flight_offers(**params)
    redis.set(
        __get_flight_offers_cache_key(**params),
        json.dumps(token),
        ttl=__get_flight_offers_cache_ttl()
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

