import unittest

from watergrid.context import DataContext, OutputMode
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step

class MockSplitStep(Step):
    def __init__(self, test_data: list):
        super().__init__(self.__class__.__name__, provides=['test_data'])
        self.__test_data = test_data

    def run(self, context: DataContext):
        context.set('test_data', self.__test_data)
        context.set_output_mode(OutputMode.SPLIT)

class MockStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.mock_flag = 0

    def run(self, context: DataContext):
        self.mock_flag += 1

    def get_flag(self):
        return self.mock_flag

class MockVerifyStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.mock_flag = 0

    def run(self, context: DataContext):
        self.mock_flag += context.get('test_data')

    def get_flag(self):
        return self.mock_flag

class DataContextTestCase(unittest.TestCase):
    def test_normal_context_runs_once(self):
        step1 = MockStep()
        step2 = MockStep()
        pipeline = Pipeline("test_pipeline")
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        pipeline.run()
        self.assertEqual(1, step1.get_flag())
        self.assertEqual(1, step2.get_flag())

    def test_split_context_runs_twice(self):
        step1 = MockSplitStep(test_data=[0, 1])
        step2 = MockStep()
        pipeline = Pipeline("test_pipeline")
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        pipeline.run()
        self.assertEqual(2, step2.get_flag())

    def test_split_context_splits_data(self):
        step1 = MockSplitStep(test_data=[1, 3, 5, 7, 9])
        step2 = MockVerifyStep()
        pipeline = Pipeline("test_pipeline")
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        pipeline.run()
        self.assertEqual(25, step2.get_flag())


if __name__ == '__main__':
    unittest.main()
