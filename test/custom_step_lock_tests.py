import unittest

from watergrid.context import DataContext
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step


class MockSetLockStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__)

    def run(self, context: DataContext):
        if not context.lock.acquire():
            raise Exception("Unable to obtain lock")


class MockVerifyStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.mock_flag = False

    def run(self, context: DataContext):
        self.mock_flag = context.lock.has_lock()

    def get_flag(self) -> bool:
        return self.mock_flag


class CustomStepLockTestCase(unittest.TestCase):
    def test_can_use_lock(self):
        mock_step = MockVerifyStep()
        pipeline = Pipeline("test_pipeline")
        pipeline.add_step(MockSetLockStep())
        pipeline.add_step(mock_step)
        pipeline.run()
        self.assertTrue(mock_step.get_flag())


if __name__ == '__main__':
    unittest.main()
