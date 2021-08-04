from time import time

from redis import Redis

from app.config import REDIS_URL


if __name__ == "__main__":
    start = time()
    redis = Redis.from_url(REDIS_URL)
    for key in [key.decode() for key in redis.keys("*")]:
        print(f"Delete : {key}")
        redis.delete(key)

    print(f"Completed. : {time() - start:.2f}s")
