from abc import ABC

from watergrid.context import DataContext, OutputMode
from watergrid.steps import Step


class Pipeline(ABC):
    """
    Internal class that represents a pipeline of steps.

    :param pipeline_name: Name of the pipeline.
    :type pipeline_name: str
    """

    def __init__(self, pipeline_name: str):
        self._pipeline_name = pipeline_name
        self._steps = []
        self._metrics_exporters = []

    def add_step(self, step: Step):
        """
        Add a step to the pipeline.

        :param step: Step to add.
        :type step: Step
        """
        self._steps.append(step)

    def run(self):
        """
        Blocking operation that runs all steps in the pipeline once.
        :return: None
        """
        self.verify_pipeline()
        for metrics_exporter in self._metrics_exporters:
            metrics_exporter.start_pipeline(self._pipeline_name)
        contexts = [DataContext()]
        next_contexts = []
        for step in self._steps:
            for context in contexts:
                for metrics_exporter in self._metrics_exporters:
                    metrics_exporter.start_step(step.get_step_name())
                step.run_step(context)
                for metrics_exporter in self._metrics_exporters:
                    metrics_exporter.end_step(step.get_step_name())
                if context.get_output_mode() == OutputMode.SPLIT:
                    split_key = step.get_step_provides()[0] # TODO: handle split matrix
                    split_value = context.get(split_key)
                    for value in split_value:
                        new_context = DataContext()
                        new_context.set_batch(dict(context.get_all()))
                        new_context.set(split_key, value)
                        next_contexts.append(new_context)
                elif context.get_output_mode() == OutputMode.FILTER and (context.get(step.get_step_provides()[0]) is None):
                    continue
                else:
                    new_context = DataContext()
                    new_context.set_batch(dict(context.get_all()))
                    next_contexts.append(new_context)
            contexts = next_contexts
            next_contexts = []
        for metrics_exporter in self._metrics_exporters:
            metrics_exporter.end_pipeline(self._pipeline_name)


    def get_step_count(self):
        """
        :return: Number of steps in the pipeline.
        """
        return len(self._steps)

    def get_pipeline_name(self) -> str:
        """
        :return: Name of the pipeline.
        """
        return self._pipeline_name

    def verify_pipeline(self):
        """
        Verifies that the pipeline is valid and that all step dependencies are met.
        :return: None
        """
        self.__verify_pipeline_dependencies_fulfilled()
        self.__verify_step_ordering()

    def __verify_pipeline_dependencies_fulfilled(self):
        """
        Verifies that all dependencies of the pipeline are fulfilled by at least one other step. Does not check
        validity of step ordering in the pipeline.
        :return: None
        """
        # Get a list of all provided data keys.
        provided_keys = []
        for step in self._steps:
            for step_provider in step.get_step_provides():
                if step_provider not in provided_keys:
                    provided_keys.append(step_provider)
        # Check that all dependencies are met
        for step in self._steps:
            for step_dependency in step.get_step_requirements():
                if step_dependency not in provided_keys:
                    raise Exception(f"Step {step.get_step_name()} requires {step_dependency} to be provided.")

    def __verify_step_ordering(self):
        """
        Verifies that all steps in the pipeline are in the correct order.
        :return: None
        """
        # Get a list of all provided data keys.
        provided_keys = []
        step_index = 0
        index_hop_count = 0
        while step_index < len(self._steps):
            index_hop_count += 1
            if index_hop_count > len(self._steps) ** 2:
                raise Exception("Unable to resolve step dependencies.")
            index_moved = False
            for step_dependency in self._steps[step_index].get_step_requirements():
                if step_dependency not in provided_keys:
                    self._steps.append(self._steps.pop(step_index))
                    index_moved = True
                    break
            if not index_moved:
                for provided_key in self._steps[step_index].get_step_provides():
                    provided_keys.append(provided_key)
                step_index += 1

    def add_metrics_exporter(self, exporter):
        self._metrics_exporters.append(exporter)

