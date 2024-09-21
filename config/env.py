import os


def get_env_variable(key):
    return os.environ.get(key) or None
