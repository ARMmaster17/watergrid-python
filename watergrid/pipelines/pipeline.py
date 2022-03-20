from abc import ABC

from watergrid.context import DataContext


class Pipeline(ABC):
    """
    Internal class that represents a pipeline of steps.

    :param pipeline_name: Name of the pipeline.
    :type pipeline_name: str
    """
    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.steps = []

    def add_step(self, step):
        """
        Add a step to the pipeline.

        :param step: Step to add.
        :type step: Step
        """
        self.steps.append(step)

    def run(self):
        """
        Blocking operation that runs all steps in the pipeline once.
        :return: None
        """

        context = DataContext()
        for step in self.steps:
            step.run_step(context)