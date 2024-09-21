from config.env import get_env_variable
from exception import HttpException, AmadeusException
from integration.amadeus.auth_token_cache import get_cached_auth_token, create_auth_token_cache
from integration.http import HttpClient


def __get_access_token():
    token_resp = get_cached_auth_token()
    auth_header = token_resp['token_type'] + ' ' + token_resp['access_token']
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
        "adults": 1
    }
    try:
        resp = HttpClient.get(url, headers=__get_header(), query_params=params)
    except HttpException as e:
        msg = ''
        data = e.message
        for err in data.get('errors') or []:
            if err["code"] == 38192 and retry:
                create_auth_token_cache()
                return get_flight_offers(
                    origin_location_code,
                    destination_location_code,
                    departure_date, retry=False
                )
            msg = msg + err['detail']
        raise AmadeusException(msg)
    return resp
