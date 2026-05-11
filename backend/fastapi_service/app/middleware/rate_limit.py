from slowapi import Limiter
from slowapi.util import get_remote_address


def get_limiter():
    return Limiter(key_func=get_remote_address)
