StandalonePipeline
==================

In standalone mode, only one instance of your application is required. This mode is the easiest to set up,
but does not provide any fault tolerance or host failover. If you are just getting started, this is the pipeline
mode to start with.

Steps
-----

1. Install WaterGrid-Python `pip install watergrid--1.0.1`
2. Create a pipeline and run it.

.. code-block:: python

    from watergrid.pipelines.standalone_pipeline import StandalonePipeline
    from watergrid.steps import Step
    from watergrid.context import DataContext

    class SampleStep(Step):
        def __init__(self):
            super().__init__(self.__class__.__name__)

        def run(self, context: DataContext):
            print("Hello World!")

    def main():
        pipeline = StandalonePipeline('sample_pipeline')
        pipeline.add_step(SampleStep())
        while True:
            pipeline.run()


    if __name__ == '__main__':
        main()