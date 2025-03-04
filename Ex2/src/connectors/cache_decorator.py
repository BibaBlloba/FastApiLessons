import json
from functools import wraps

from src.init import redis_manager


def custom_cache(expire: int | None = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}"

            cached_result = await redis_manager.get(key)
            if not cached_result:
                result = await func(*args, **kwargs)
                await redis_manager.set(key, str(result))
                return result

            return json.loads(cached_result)

        return wrapper

    return decorator
