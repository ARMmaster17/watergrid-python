import time

from watergrid.middleware.PipelineMiddlware import PipelineMiddleware


class LastRunMiddleware(PipelineMiddleware):
    @property
    def last_run(self):
        return self._last_run

    def pre_pipeline(self, pipeline):
        pass

    def post_pipeline(self, pipeline):
        self._last_run = time.time()

    def __init__(self):
        super().__init__()
        self._last_run = None
