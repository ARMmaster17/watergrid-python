import unittest

from watergrid.context import DataContext
from watergrid.metrics.MetricsExporter import MetricsExporter
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step


class MockMetricsExporter(MetricsExporter):
    def start_pipeline(self, pipeline_name):
        self.__pipeline_start = True

    def end_pipeline(self, pipeline_name):
        self.__pipeline_end = True

    def start_step(self, step_name):
        self.__step_start += 1

    def end_step(self, step_name):
        self.__step_end += 1

    def metrics_match(self):
        return self.__pipeline_start and self.__pipeline_end and self.__step_start == self.__step_count and self.__step_end == self.__step_count

    def __init__(self, step_count):
        self.__pipeline_start = False
        self.__pipeline_end = False
        self.__step_start = 0
        self.__step_end = 0
        self.__step_count = step_count
        super().__init__()

class MockStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.mock_flag = False

    def run(self, context: DataContext):
        self.mock_flag = True

    def get_flag(self):
        return self.mock_flag


class PipelineMetricsTestCase(unittest.TestCase):
    def test_pipeline_accepts_metrics(self):
        pipeline = Pipeline('test_pipeline')
        exporter = MockMetricsExporter(1)
        pipeline.add_metrics_exporter(exporter)
        step1 = MockStep()
        pipeline.add_step(step1)
        pipeline.run()
        self.assertTrue(step1.get_flag())
        self.assertTrue(exporter.metrics_match())

    def test_pipeline_measures_two_steps(self):
        pipeline = Pipeline('test_pipeline')
        exporter = MockMetricsExporter(2)
        pipeline.add_metrics_exporter(exporter)
        step1 = MockStep()
        step2 = MockStep()
        pipeline.add_step(step1)
        pipeline.add_step(step2)
        pipeline.run()
        self.assertTrue(step1.get_flag())
        self.assertTrue(step2.get_flag())
        self.assertTrue(exporter.metrics_match())



if __name__ == '__main__':
    unittest.main()
