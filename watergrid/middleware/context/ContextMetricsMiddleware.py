from watergrid.context import DataContext
from watergrid.metrics.MetricsStore import MetricsStore
from watergrid.middleware.ContextMiddleware import ContextMiddleware
from watergrid.steps import Step


class ContextMetricsMiddleware(ContextMiddleware):
    def pre_context(self, step: Step, context: DataContext):
        self._store.start_step_monitoring(step.get_step_name())

    def post_context(self, step: Step, context: DataContext):
        self._store.stop_step_monitoring()

    def __init__(self, store: MetricsStore):
        super().__init__()
        self._store = store
