import unittest

from watergrid.context import DataContext
from watergrid.locks import MockPipelineLock
from watergrid.pipelines import HAPipeline
from watergrid.steps import Step


class MockStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.mock_flag = False

    def run(self, context: DataContext):
        self.mock_flag = True

    def get_flag(self):
        return self.mock_flag


class HAPipelineTestCase(unittest.TestCase):
    def test_pipeline_does_not_runs_without_lock(self):
        step1 = MockStep()
        step2 = MockStep()
        mock_lock = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", mock_lock)
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        mock_lock.manual_lock()
        pipeline.run()
        self.assertFalse(step1.get_flag())
        self.assertFalse(step2.get_flag())

    def test_pipeline_runs_with_lock(self):
        step1 = MockStep()
        step2 = MockStep()
        mock_lock = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", mock_lock)
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        pipeline.run()
        self.assertTrue(step1.get_flag())
        self.assertTrue(step2.get_flag())

    def test_pipeline_releases_lock(self):
        step1 = MockStep()
        step2 = MockStep()
        mock_lock = MockPipelineLock()
        pipeline = HAPipeline("test_pipeline", mock_lock)
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        pipeline.run()
        self.assertFalse(mock_lock.has_lock())

    def test_pipeline_calculates_redis_delay(self):
        pipeline = HAPipeline("test_pipeline", MockPipelineLock())
        pipeline._append_timing(10000)
        pipeline._append_timing(20000)
        self.assertEqual(15000, pipeline.get_average_lock_delay())

    def test_pipeline_calculates_job_interval_delay(self):
        pipeline = HAPipeline("test_pipeline", MockPipelineLock())
        self.assertEqual(3000, pipeline._calculate_delay(10))


if __name__ == "__main__":
    unittest.main()
