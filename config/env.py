import os


def get_env_variable(key):
    return os.environ.get(key) or None


def set_env_variables():
    os.environ["AMADEUS_API_HOST"] = "https://test.api.amadeus.com"
    os.environ["AMADEUS_TOKEN_API_URI"] = "/v1/security/oauth2/token"
    os.environ["AMADEUS_FLIGHT_OFFERS_API_URI"] = "/v2/shopping/flight-offers"
    os.environ["AMADEUS_FLIGHT_OFFERS_CACHE_TTL"] = "600"
    os.environ["AMADEUS_ACCESS_TOKEN_CACHE_TTL"] = "1800"

    os.environ["REDIS_TTL"] = "1800"

