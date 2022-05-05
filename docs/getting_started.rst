Getting Started
===============

1. Dependencies
---------------

Run the following command in your terminal to install the required dependencies:

.. code-block:: bash

   pip install watergrid

2. Create A Watergrid Pipeline
------------------------------

Create a file called ``main.py`` and paste the following code into it:

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
       pipeline = StandalonePipeline('tutorial_pipeline')
       pipeline.add_step(SampleStep())
       pipeline.run()

    if __name__ == '__main__':
       main()


This code creates a pipeline called ``tutorial_pipeline`` and adds a step to it. When running in standalone mode, you
can name your pipeline whatever you want. The single step in this pipeline is the ``SampleStep`` class. Every time this
step runs, it prints "Hello World!" to stdout.

The command ``pipeline.run()`` just runs the pipeline once, but there are
other functions that allow for running according to a cron schedule, a specified time interval, or to just run
continuously.