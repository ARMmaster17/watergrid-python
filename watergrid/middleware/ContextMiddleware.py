from abc import abstractmethod, ABC

from watergrid.context import DataContext
from watergrid.steps import Step


class ContextMiddleware(ABC):
    """
    Abstract class representing an action that is run before and after
    every context run within each step in a pipeline.
    """

    def __init__(self):
        pass

    @abstractmethod
    def pre_context(self, step: Step, context: DataContext):
        pass

    @abstractmethod
    def post_context(self, step: Step, context: DataContext):
        pass
