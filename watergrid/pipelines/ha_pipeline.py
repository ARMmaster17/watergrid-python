import logging
import time

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

    def run_scheduled(self, job_interval_s: int):
        self.verify_pipeline()
        if self.__pipeline_lock.lock():
            last_run = self.__pipeline_lock.read_key("{}_last_run".format(self.get_pipeline_name()))
            if last_run is None:
                self.__pipeline_lock.write_key("{}_last_run".format(self.get_pipeline_name()), time.perf_counter() - job_interval_s)
            if time.perf_counter() - last_run > job_interval_s * 3:
                logging.warning(
                    "Pipeline {} has fallen more than three cycles behind. Consider increasing the job interval or "
                    "provisioning more machines.".format(
                        self.get_pipeline_name()
                    )
                )
                self.__pipeline_lock.write_key("{}_last_run".format(self.get_pipeline_name()), time.perf_counter() - job_interval_s)
            if time.perf_counter() - last_run > job_interval_s:
                super().run()
                self.__pipeline_lock.write_key("{}_last_run".format(self.get_pipeline_name()), last_run + job_interval_s)
            self.__pipeline_lock.unlock()
        else:
            logging.debug(
                "Pipeline {} is already running on another instance".format(
                    self.get_pipeline_name()
                )
            )
