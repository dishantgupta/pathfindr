

import redis

from config.env import get_env_variable


def __get_redis_host():
    return get_env_variable("REDIS_HOST")


def __get_redis_port():
    return int(get_env_variable("REDIS_PORT"))


def __get_redis_ttl():
    return get_env_variable("REDIS_TTL")


def __get_redis():
    return redis.Redis(
        host=__get_redis_host(),
        port=__get_redis_port(),
        db=0
    )


__pool = redis.ConnectionPool(
    host=__get_redis_host(),
    port=__get_redis_port(),
    db=0,
    max_connections=20
)
__redis = redis.Redis(connection_pool=__pool)


def set(k, v, ttl=None):
    return __redis.set(k, v, ex=ttl or __get_redis_ttl())


def get(k):
    return __redis.get(k)
