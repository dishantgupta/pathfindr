from config.env import get_env_variable
from integration.http import HttpClient


def __get_api_key():
    api_key = get_env_variable("AMADEUS_API_KEY")
    return api_key


def __get_api_secret_key():
    api_secret_key = get_env_variable("AMADEUS_API_SECRET_KEY")
    return api_secret_key


def __get_amadeus_api_host():
    api_host = get_env_variable("AMADEUS_API_HOST")
    return api_host


def __get_headers():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return headers


def __get_payload():
    payload = {
        "grant_type": "client_credentials",
        "client_id": __get_api_key(),
        "client_secret": __get_api_secret_key()
    }
    return payload


def __get_uri():
    uri = get_env_variable("AMADEUS_TOKEN_API_URI")
    return uri


def create_access_token():
    url = __get_amadeus_api_host() + __get_uri()
    resp = HttpClient.post(
        url, __get_payload(), __get_headers()
    )
    return resp



"""

curl "https://test.api.amadeus.com/v1/security/oauth2/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

"""


