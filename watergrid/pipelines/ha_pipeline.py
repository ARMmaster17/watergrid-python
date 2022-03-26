import logging

from watergrid.context import DataContext
from watergrid.locks import PipelineLock
from watergrid.pipelines.pipeline import Pipeline


class HAPipeline(Pipeline):
    """
    The high availability pipeline allows for several machines to have the pipeline loaded at once. If one of the
    machines fails, or if the pipeline context times out, the pipeline will run on another machine.

    :param pipeline_name: The name of the pipeline.
    :param redis_host: The host of the redis server.
    :param redis_port: The port of the redis server.
    :param redis_db: The database of the redis server.
    :param lock_timeout: The length of time granted with a global lock. Should be set to a value that is high enough to
        allow for the pipeline to finish under a single lock.
    """

    def __init__(self, pipeline_name: str, pipeline_lock: PipelineLock):
        self.__pipeline_lock = pipeline_lock
        super().__init__(pipeline_name)

    def run(self):
        self.verify_pipeline()
        if self.__pipeline_lock.lock():
            context = DataContext()
            for step in self._steps:
                self.__pipeline_lock.ping()
                step.run_step(context)
            self.__pipeline_lock.unlock()
        else:
            logging.debug(
                "Pipeline {} is already running on another instance".format(
                    self.get_pipeline_name()
                )
            )
