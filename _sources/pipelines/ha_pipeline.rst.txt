HAPipeline
==================

In HA mode, you can have several servers running on separate machines. Only
one server will be able to run the pipeline at a time. If a machine fails, another will take over.

Steps
-----

1. Install WaterGrid-Python `pip install watergrid==1.0.1`
2. Install Redis (or use the `PipelineLock` class to create your own global mutex).
3. Create a pipeline and run it.

.. code-block:: python

    from watergrid.pipelines import HAPipeline
    from watergrid.steps import Step
    from watergrid.context import DataContext
    from watergrid.locks import RedisPipelineLock

    class SampleStep(Step):
        def __init__(self):
            super().__init__(self.__class__.__name__)

        def run(self, context: DataContext):
            print("Hello World!")

    def main():
        pipeline_name = "sample_pipeline"
        redis_lock = RedisPipelineLock()
        # Call redis_lock.set_XXXX to configure connection properties if needed.
        redis_lock.connect() # Required by RedisPipelineLock, does not apply to all locks.
        pipeline = HAPipeline(pipeline_name, redis_lock)
        pipeline.add_step(SampleStep())
        while True:
            pipeline.run()


    if __name__ == '__main__':
        main()

If Redis is not running on localhost on port 6379, you can call `redis_lock.set_XXXX()` to set those values accordingly.
