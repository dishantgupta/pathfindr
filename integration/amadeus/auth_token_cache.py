import json

from cache import redis
from integration.amadeus.auth_token import create_access_token


TOKEN_TTL = 1800

def __get_auth_token_cache_key():
    return "amadeus_access_token"


def create_auth_token_cache():
    token = create_access_token()
    redis.set(__get_auth_token_cache_key(), json.dumps(token), ttl=TOKEN_TTL)


def __get_auth_token_cache():
    token = redis.get(__get_auth_token_cache_key())
    return token


def get_auth_token():
    token = redis.get(__get_auth_token_cache_key())
    if not token:
        create_auth_token_cache()
        token = redis.get(__get_auth_token_cache_key())

    token = json.loads(token)
    return token


