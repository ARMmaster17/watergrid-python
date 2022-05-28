from watergrid.metrics.MetricsStore import MetricsStore
from watergrid.middleware.PipelineMiddlware import PipelineMiddleware


class PipelineMetricsMiddleware(PipelineMiddleware):
    def __init__(self, store: MetricsStore):
        super().__init__()
        self._store = store

    def pre_pipeline(self, pipeline):
        self._store.start_pipeline_monitoring(pipeline.get_pipeline_name())

    def post_pipeline(self, pipeline):
        self._store.stop_pipeline_monitoring()
