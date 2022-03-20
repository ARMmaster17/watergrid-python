from abc import ABC, abstractmethod

from watergrid.context import DataContext


class Step(ABC):
    """
    Abstract class for a single step in a pipeline.

    :param step_name: Name of the step.
    :type step_name: str
    """
    def __init__(self, step_name: str):
        self.step_name = step_name

    def run_step(self, context: DataContext):
        """
        Used internally by the pipeline. Performs setup and teardown
        in addition to running the step function run().
        :return: None
        """
        self.run(context)

    @abstractmethod
    def run(self, context: DataContext):
        pass