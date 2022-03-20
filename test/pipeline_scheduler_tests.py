import unittest

from watergrid.context import DataContext
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step


class MockStep(Step):
    def __init__(self, provides=[], requires=[]):
        super().__init__(self.__class__.__name__)
        self.run_order = 0

    def run(self, context: DataContext):
        if context.has('test_key'):
            self.run_order = context.get('test_key') + 1
            context.set('test_key', self.run_order)
        else:
            context.set('test_key', 1)
            self.run_order = 1

    def get_flag(self):
        return self.run_order


class PipelineSchedulerTestCase(unittest.TestCase):
    def test_pipeline_does_not_break_in_order_steps(self):
        pipeline = Pipeline('test_pipeline')
        step_a = MockStep(provides=['a'])
        pipeline.add_step(step_a)
        step_b = MockStep(requires=['b'])
        pipeline.add_step(step_b)
        pipeline.run()
        self.assertEqual(step_a.get_flag(), 1)
        self.assertEqual(step_b.get_flag(), 2)


if __name__ == '__main__':
    unittest.main()
