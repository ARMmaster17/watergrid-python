from watergrid.locks import PipelineLock


class MockPipelineLock(PipelineLock):
    def __init__(self, lock_timeout: int = 60):
        super().__init__(lock_timeout)
        self.external_lock = False
        self.client_lock = False

    def manual_lock(self):
        self.external_lock = True
        self.client_lock = False

    def manual_unlock(self):
        self.external_lock = False

    def acquire(self) -> bool:
        if not self.external_lock:
            self.client_lock = True
            return True
        else:
            return False

    def has_lock(self) -> bool:
        return self.client_lock

    def extend_lease(self):
        pass

    def release(self):
        self.client_lock = False
