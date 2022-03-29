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
        super().__init__(pipeline_name)
        self.__pipeline_lock = pipeline_lock
        self.__lock_timings = []

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

    def run_interval(self, job_interval_s: int):
        self.verify_pipeline()
        while True:
            if self.__pipeline_lock.lock():
                last_run = float(self.__pipeline_lock.read_key("{}_last_run".format(self.get_pipeline_name())).decode("utf-8"))
                if last_run is None:
                    self.__pipeline_lock.write_key("{}_last_run".format(self.get_pipeline_name()), time.time() - job_interval_s)
                if time.time() - last_run > job_interval_s * 3:
                    logging.warning(
                        "Pipeline {} has fallen more than three cycles behind. Consider increasing the job interval or "
                        "provisioning more machines.".format(
                            self.get_pipeline_name()
                        )
                    )
                    self.__pipeline_lock.write_key("{}_last_run".format(self.get_pipeline_name()), time.time() - job_interval_s)
                if time.time() - last_run > job_interval_s:
                    super().run()
                    self.__pipeline_lock.write_key("{}_last_run".format(self.get_pipeline_name()), last_run + job_interval_s)
                self.__pipeline_lock.unlock()
            else:
                logging.debug(
                    "Pipeline {} is already running on another instance".format(
                        self.get_pipeline_name()
                    )
                )
            time.sleep(self._calculate_delay(job_interval_s) / 1000)

    def lock_with_timing(self):
        start_time = time.perf_counter()
        self.__pipeline_lock.lock()
        self._append_timing(time.perf_counter() - start_time)

    def unlock_with_timing(self):
        start_time = time.perf_counter()
        self.__pipeline_lock.unlock()
        self._append_timing(time.perf_counter() - start_time)

    def get_average_lock_delay(self) -> float:
        if len(self.__lock_timings) == 0:
            return 0
        return float(sum(self.__lock_timings)) / float(len(self.__lock_timings))

    def _calculate_delay(self, pipeline_interval_s: int, checks_per_interval: int = 10, check_ratio: int = 3) -> int:
        redis_delay_ms = self.get_average_lock_delay()
        job_delay_ms = float(pipeline_interval_s * 1000) / float(checks_per_interval)
        if redis_delay_ms > job_delay_ms:
            logging.warning("Slow redis cluster detected. Consider increasing the size of your cluster.")
        return int(max(redis_delay_ms, job_delay_ms)) * check_ratio

    def _append_timing(self, timing: float):
        self.__lock_timings.append(timing)
        if len(self.__lock_timings) > 100:
            self.__lock_timings.pop(0)
