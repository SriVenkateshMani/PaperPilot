import redis

redis_client = redis.Redis(
    host = "redis",
    port = 6379,
    decode_responses = True
)

def get_cache(key: str):
    return redis_client.get(key)

def set_cache(key: str, value: str, ttl: int = 21600):
    redis_client.setex(key, ttl, value)