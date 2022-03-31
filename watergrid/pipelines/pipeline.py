import time
from abc import ABC

import pycron

from watergrid.context import DataContext, OutputMode
from watergrid.metrics.MetricsStore import MetricsStore
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
        self._metrics_store = MetricsStore()

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
        self._metrics_store.start_pipeline_monitoring(self._pipeline_name)
        try:
            self.__run_pipeline_steps()
        except Exception as e:
            self._metrics_store.report_exception(e)
            self._metrics_store.stop_step_monitoring()
        finally:
            self._metrics_store.stop_pipeline_monitoring()

    def run_loop(self):
        """
        Runs the pipeline in a loop. Subsequent executions will run immediately after the previous execution.
        """
        while True:
            self.run()

    def run_scheduled(self, cron_expression: str):
        """
        Runs the pipeline once every time the cron expression matches.

        :param cron_expression: Cron expression to match.
        :type cron_expression: str
        """
        while True:
            if pycron.is_now(cron_expression):
                start_time = time.perf_counter()
                self.run()
                elapsed_time = time.perf_counter() - start_time
                time.sleep(
                    60 - elapsed_time
                )  # Sleep for the remaining time in the minute so that the pipeline does not run multiple times per cron trigger.
            else:
                time.sleep(1)

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
        provided_keys = self.__get_all_step_provides()
        # Check that all dependencies are met
        self.__check_for_unlinked_dependencies(provided_keys)

    def __get_all_step_provides(self) -> list:
        """
        Gets a list of all unique keys provided by all steps in the pipeline.
        :return: List of all data keys provided by all steps in the pipeline.
        """
        provides = []
        for step in self._steps:
            for step_provider in step.get_step_provides():
                if step_provider not in provides:
                    provides.append(step_provider)
        return provides

    def __check_for_unlinked_dependencies(self, provided_keys: list):
        for step in self._steps:
            for step_dependency in step.get_step_requirements():
                if step_dependency not in provided_keys:
                    raise Exception(
                        f"Step {step.get_step_name()} requires {step_dependency} to be provided."
                    )

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
        """
        Adds a metrics exporter to the pipeline metric store.
        :param exporter: Exporter to add.
        :return: None
        """
        self._metrics_store.add_metrics_exporter(exporter)

    def __run_pipeline_steps(self):
        """
        Performs setup and runs all steps in the pipeline.
        :return:
        """
        contexts = [DataContext()]
        for step in self._steps:
            contexts = self.__run_step_for_each_context(step, contexts)

    def __run_step_for_each_context(self, step: Step, context_list: list) -> list:
        """
        Runs the given step once for each context in the context list and performs post-processing.
        :param step: Step to run.
        :param context_list: List of contexts to provide to the step runtime.
        :return: List of contexts to provide to the next step.
        """
        next_contexts = []
        for context in context_list:
            self.__run_step_with_performance_monitoring(step, context)
            self.__process_step_output(context, step.get_step_provides(), next_contexts)
        return next_contexts

    def __process_step_output(
        self, context: DataContext, step_provides: list, next_contexts: list
    ):
        """
        Performs post-processing on the output of a step.
        :param context: Output from the current step.
        :param step_provides: List of data keys that the step provides.
        :param next_contexts: List of contexts that will be passed to the next step.
        :return: None
        """
        if context.get_output_mode() == OutputMode.SPLIT:
            self.__split_context(step_provides, context, next_contexts)
        elif context.get_output_mode() == OutputMode.FILTER:
            self.__filter_context(step_provides, context, next_contexts)
        else:
            self.__forward_context(context, next_contexts)

    def __run_step_with_performance_monitoring(self, step: Step, context: DataContext):
        """
        Runs a single step in the pipeline and forwards performance data to any installed monitoring plugins.
        :param step: Step to run.
        :param context: Context to provide to the step runtime.
        :return: None
        """
        self._metrics_store.start_step_monitoring(step.get_step_name())
        step.run_step(context)
        self._metrics_store.stop_step_monitoring()

    def __split_context(
        self, step_provides: list, context: DataContext, next_contexts: list
    ):
        """
        Splits the context into multiple contexts based on the output of the current step.
        :param step_provides: The list of data keys that the current step provides.
        :param context: The context instance from the current step.
        :param next_contexts: The list of contexts that will be passed to the next step.
        :return: None
        """
        split_key = step_provides[0]
        split_value = context.get(split_key)
        for value in split_value:
            new_context = self.__deep_copy_context(context)
            new_context.set(split_key, value)
            next_contexts.append(new_context)

    def __filter_context(
        self, step_provides: list, context: DataContext, next_contexts: list
    ):
        """
        Forwards the context to the next step if the given filter key is present.
        :param step_provides: The list of context keys that the step provides.
        :param context: The context instance from the current step.
        :param next_contexts: The list of contexts that will be passed to the next step.
        :return: None
        """
        if context.get(step_provides[0]) is not None:
            next_contexts.append(self.__deep_copy_context(context))

    def __forward_context(self, context: DataContext, next_contexts: list):
        """
        Forwards the context to the next step with no post-processing.
        :param context: Context to forward.
        :param next_contexts: List of contexts that will be used by the next step.
        :return: None
        """
        next_contexts.append(self.__deep_copy_context(context))

    @staticmethod
    def __deep_copy_context(context: DataContext):
        """
        Creates a deep copy of a DataContext object.
        :param context: Context instance to be copied.
        :return: New copy of the given context instance.
        """
        new_context = DataContext()
        new_context.set_batch(dict(context.get_all()))
        return new_context
