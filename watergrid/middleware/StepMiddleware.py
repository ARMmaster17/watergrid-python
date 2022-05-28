from abc import ABC, abstractmethod

from watergrid.steps import Step


class StepMiddleware(ABC):
    """
    Abstract class representing an action that runs before and after each
    action.
    """

    def __init__(self):
        pass

    @abstractmethod
    def pre_step(self, step: Step, contexts: list) -> None:
        pass

    @abstractmethod
    def post_step(self, step: Step, contexts: list) -> None:
        pass
