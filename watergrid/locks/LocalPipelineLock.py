from watergrid.locks.PipelineLock import PipelineLock


class LocalPipelineLock(PipelineLock):
    def acquire(self) -> bool:
        if not self._lock_obj:
            self._lock_obj = True
            return True
        else:
            return False

    def has_lock(self) -> bool:
        return self._lock_obj

    def extend_lease(self):
        pass

    def release(self):
        self._lock_obj = False

    def read_key(self, key: str):
        return self.__key_value[key]

    def write_key(self, key: str, value):
        self.__key_value[key] = value

    def __init__(self, lock_timeout: int = 60):
        super().__init__(lock_timeout)
        self._lock_obj = False
        self.__key_value = {}