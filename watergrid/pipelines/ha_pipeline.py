import logging

from watergrid.context import DataContext
from watergrid.locks.PipelineLock import PipelineLock
from watergrid.pipelines.pipeline import Pipeline


class HAPipeline(Pipeline):
    """
    The high availability pipeline allows for several machines to have the pipeline loaded at once. If one of the
    machines fails, or if the pipeline context times out, the pipeline will run on another machine.

    :param pipeline_name: The name of the pipeline.
    :param pipeline_lock: The lock implementation to use for this pipeline.
    """

    def __init__(self, pipeline_name: str, pipeline_lock: PipelineLock):
        self.__pipeline_lock = pipeline_lock
        super().__init__(pipeline_name)

    def run(self):
        self.verify_pipeline()
        if self.__pipeline_lock.lock():
            super().run()
            self.__pipeline_lock.unlock()
        else:
            logging.debug(
                "Pipeline {} is already running on another instance".format(
                    self.get_pipeline_name()
                )
            )
