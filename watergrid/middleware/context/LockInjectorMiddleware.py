from watergrid.context import DataContext
from watergrid.locks.LocalPipelineLock import LocalPipelineLock
from watergrid.middleware.ContextMiddleware import ContextMiddleware
from watergrid.steps import Step


class LockInjectorMiddleware(ContextMiddleware):
    """
    Modifies a context before an after a step to ensure that the lock context
    is not deep copied as when using local locks this will break the
    functionality of the lock.
    """
    def pre_context(self, step: Step, context: DataContext):
        context.lock = self._pipeline.lock

    def post_context(self, step: Step, context: DataContext):
        context.lock = None

    def __init__(self, pipeline):
        super().__init__()
        self._pipeline = pipeline
