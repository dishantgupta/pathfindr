import json
import logging

from cache import redis
from config.env import get_env_variable
from integration.amadeus.auth_token import create_access_token

logger = logging.getLogger(__name__)


def __get_auth_token_cache_ttl():
    return int(get_env_variable("AMADEUS_ACCESS_TOKEN_CACHE_TTL") or 1800)


def __get_auth_token_cache_key():
    return "amadeus_access_token"


def create_auth_token_cache():
    token_resp = create_access_token()
    auth_header = token_resp['token_type'] + ' ' + token_resp['access_token']
    redis.set(
        __get_auth_token_cache_key(),
        auth_header, ttl=__get_auth_token_cache_ttl()
    )


def get_cached_auth_token():
    token = redis.get(__get_auth_token_cache_key())
    if not token:
        logger.debug("AMADEUS access token not found in cache, generating token")
        create_auth_token_cache()
        logger.debug("AMADEUS access token not found in cache, token generated, cache set")
        token = redis.get(__get_auth_token_cache_key())
    return token


