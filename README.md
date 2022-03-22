# WaterGrid-Python
Lightweight distributed framework for data stream processing.

# Getting Started
## Standalone Mode
In standalone mode, 
1. Install WaterGrid-Python `pip install git+https://github.com/ARMmaster17/watergrid-python.git@main`
2. Create a pipeline and run it.
```python
from watergrid.pipelines import StandalonePipeline
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
```

## High Availability Mode
In HA mode, you can have several servers running on separate machines. Only
one server will be able to run the pipeline at a time. If a machine fails, another will take over.

1. Install WaterGrid-Python `pip install git+https://github.com/ARMmaster17/watergrid-python.git@main`
2. Install Redis on another server (or use the `PipelineLock` to create your own global mutex).
3. Create a pipeline and run it.
```python
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
    redis_lock = RedisPipelineLock(
        lock_key=pipeline_name,
        redis_host='localhost',
        redis_port=6379,
        redis_db=0,
        redis_password=None,
        lock_timeout=60, # This is the maximum time a single step can run.
    )
    pipeline = HAPipeline(pipeline_name, redis_lock)
    pipeline.add_step(SampleStep())
    while True:
        pipeline.run()

        
if __name__ == '__main__':
    main()
```
# Step Operations

## Creating Custom Steps
Every step of your pipeline should be its own class and inherit from the `Step` class. Here is an example:

```python
from watergrid.steps import Step
from watergrid.context import DataContext

class AddValueStep(Step):
    def __init__(self):
        # Use requires to denote which steps need to run before this one, and
        # use provides to denote which steps can run after this one.
        super().__init__(self.__class__.__name__, requires=['value'], provides=['added_value'])

    def run(self, context: DataContext):
        # Use the context object to pass values between steps.
        context.set('added_value', context.get('value') + 1)
```

## Split Steps
Sometimes you will have a pipeline step that will have a list of several values,
and you want to split the list so that each step will run once for each value.

```python
from watergrid.steps import Step
from watergrid.context import DataContext
from watergrid.context import OutputMode

class AddValuesStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, provides=['added_value'])

    def run(self, context: DataContext):
        context.set('added_value', [0, 1, 2, 3, 4, 5])
        context.set_output_mode(OutputMode.SPLIT)
        # The pipeline will automatically split the first key listed in provides.
        # For example, in the next step context.get('added_value') will return 0.
        # Then the next step will run again with the values 1, 2, 3, etc...
```

## Filter Steps
Filter steps have the option to pass back the value of `None`. If this is the case, this instance of the context will be deleted and not passed to the next step. Works great with split steps.

Note that the pipeline will only filter the first field listed in the provides list.

```python
from watergrid.steps import Step
from watergrid.context import DataContext
from watergrid.context import OutputMode
class FilterStep(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__, requires=['value'], provides=['filtered_value'])

    def run(self, context: DataContext):
        value = context.get('value')
        context.set_output_mode(OutputMode.FILTER)
        if value == 1:
            context.set('filtered_value', value)
        else:
            context.set('filtered_value', None)
```
