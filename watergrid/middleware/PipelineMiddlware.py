from abc import ABC, abstractmethod


class PipelineMiddleware(ABC):
    """
    Abstract class representing an action that is run before and after
    every run of the pipeline.
    """

    def __init__(self):
        pass

    @abstractmethod
    def pre_pipeline(self, pipeline):
        pass

    @abstractmethod
    def post_pipeline(self, pipeline):
        pass
