import unittest

from watergrid.locks import RedisPipelineLock


class PipelineTestCase(unittest.TestCase):
    def test_can_connect(self):
        redis_lock = RedisPipelineLock()
        redis_lock.connect()

    def test_can_cycle_lock(self):
        redis_lock = RedisPipelineLock()
        redis_lock.connect()
        redis_lock.lock()
        self.assertTrue(redis_lock.has_lock())
        redis_lock.unlock()

    def test_can_set_host(self):
        redis_lock = RedisPipelineLock()
        redis_lock.set_host("localhost")

    def test_can_set_port(self):
        redis_lock = RedisPipelineLock()
        redis_lock.set_port(6379)

    def test_can_set_db(self):
        redis_lock = RedisPipelineLock()
        redis_lock.set_db(0)

    def test_can_set_password(self):
        redis_lock = RedisPipelineLock()
        redis_lock.set_password("password")

    def test_can_renew_lock(self):
        redis_lock = RedisPipelineLock()
        redis_lock.connect()
        redis_lock.lock()
        redis_lock.extend_lease()
        redis_lock.unlock()
