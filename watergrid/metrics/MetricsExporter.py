from abc import ABC, abstractmethod


class MetricsExporter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def start_pipeline(self, pipeline_name):
        pass

    @abstractmethod
    def end_pipeline(self, pipeline_name):
        pass

    @abstractmethod
    def start_step(self, step_name):
        pass

    @abstractmethod
    def end_step(self, step_name):
        pass