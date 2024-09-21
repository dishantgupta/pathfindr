import logging

from config.env import get_env_variable
from errors.exception import HttpException, AmadeusException
from integration.amadeus.auth_token_cache import get_cached_auth_token, create_auth_token_cache
from integration.http import HttpClient

logger = logging.getLogger(__name__)


AMADEUS_UNAUTHENTICATED_ERROR_CODE = 38192


def __get_access_token():
    auth_header = get_cached_auth_token()
    return auth_header


def __get_header():
    headers = {
        "Authorization": __get_access_token()
    }
    return headers


def __get_amadeus_api_host():
    api_host = get_env_variable("AMADEUS_API_HOST")
    return api_host


def __get_uri():
    uri = get_env_variable("AMADEUS_FLIGHT_OFFERS_API_URI")
    return uri


def get_flight_offers(
        origin_location_code: str,
        destination_location_code: str,
        departure_date: str, retry=True
):
    url = __get_amadeus_api_host() + __get_uri()
    params = {
        "originLocationCode": origin_location_code,
        "destinationLocationCode": destination_location_code,
        "departureDate": departure_date,
        "adults": 1, "currencyCode": "USD"
    }
    headers = None
    try:
        headers = __get_header()

        logger.debug(
            "fetching AMADEUS Flight Offers: url: {url} params: {params}".format(
                url=url, params=params
            )
        )
        resp = HttpClient.get(url, headers=headers, query_params=params)
        logger.debug(
            "AMADEUS Flight Offers Success: url: {url} params: {params} resp: {resp}".format(
                url=url, params=params, resp=resp
            )
        )
    except HttpException as e:
        logger.error(
            "AMADEUS Flight Offers failed with error: {} url: {} params: {} header: {}".format(
                e.message, url, params, headers
            )
        )

        msg = ''
        data = e.message
        for err in data.get('errors') or []:
            if err["code"] == AMADEUS_UNAUTHENTICATED_ERROR_CODE and retry:
                logger.debug(
                    "AMADEUS Flight Offers API failed due to Token Expire. creating new token and setting cache"
                )
                create_auth_token_cache()
                logger.debug(
                    "AMADEUS Flight Offers API failed due to Token Expire. token generated"
                )
                return get_flight_offers(
                    origin_location_code,
                    destination_location_code,
                    departure_date, retry=False
                )
            msg = msg + err['detail']
        raise AmadeusException(msg)
    return resp
