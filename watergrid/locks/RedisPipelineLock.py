from redis import Redis
from redis.lock import Lock

from watergrid.locks import PipelineLock


class RedisPipelineLock(PipelineLock):
    def __init__(
        self,
        lock_key: str,
        redis_host: str,
        redis_port: int,
        redis_db: int,
        redis_password: str = None,
        lock_timeout: int = None,
    ):
        self.__redis = Redis(
            host=redis_host, port=redis_port, db=redis_db, password=redis_password
        )
        self.__lock = Lock(self.__redis, lock_key, timeout=lock_timeout)
        super().__init__(lock_timeout=lock_timeout)

    def acquire(self) -> bool:
        return self.__lock.acquire(blocking=False)

    def has_lock(self) -> bool:
        return self.__lock.owned()

    def extend_lease(self):
        self.__lock.extend(self.lock_timeout)

    def release(self):
        self.__lock.release()
