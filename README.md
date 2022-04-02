# WaterGrid-Python
[![WaterGrid Tests](https://github.com/ARMmaster17/watergrid-python/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ARMmaster17/watergrid-python/actions/workflows/ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/5ecd1367c30a9a8a5c59/maintainability)](https://codeclimate.com/github/ARMmaster17/watergrid-python/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5ecd1367c30a9a8a5c59/test_coverage)](https://codeclimate.com/github/ARMmaster17/watergrid-python/test_coverage)
![PyPI](https://img.shields.io/pypi/v/watergrid)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Lightweight distributed framework for data stream processing.

# Getting Started
## Concepts
### Pipeline
A watergrid application is composed of a single pipeline, There are two types of pipelines:
- `StandalonePipeline` - For low impact use cases where simplicity is preferred.
- `HAPipeline` - For use cases where high availability is required along with only-once processing.

### Steps
A pipeline is composed of one or more steps. Once you create a pipeline, you can add steps using the `add_step()` method.
Watergrid expects that you create a new class for each step that you want to perform in the pipeline. All steps must
inherit from the abstract `Step` class. Your steps should provide an override for the `run(context)` method. Inside this
method you can perform any actions you want.

### Context
The context is a key-value store that is passed to each step in the pipeline. You can use the context to store
data created in your step, and to access data created in previous steps. Changing the `OutputMode` of the context
in a set allows for splitting or filtering the context after the step completes. This can be used to have subsequent
steps run multiple times based on the output of the current step.

### Locks
When using the `HAPipeline` class, you must provide a lock to prevent multiple instances from running the same pipeline
at the same time. The `RedisLock` class is provided by watergrid, but you are free to implement your own lock
using the `Lock` abstract class.

## Standalone Mode
In standalone mode, only one instance of your application is required. This mode is the easiest to set up,
but does not provide any fault tolerance or host failover.
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
2. Install Redis (or use the `PipelineLock` to create your own global mutex).
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
    redis_lock = RedisPipelineLock()
    # Call redis_lock.set_XXXX to configure connection properties if needed.
    pipeline = HAPipeline(pipeline_name, redis_lock)
    pipeline.add_step(SampleStep())
    while True:
        pipeline.run()

        
if __name__ == '__main__':
    main()
```

If Redis is not running on localhost on port 6379, you can call `redis_lock.set_XXXX()` to set those values accordingly.

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
Note that the `requires` and `provides` lists are optional. If you do not specify them, the step will run
in any order in the pipeline. The keys provided in the two lists can be arbitrary, and do not need to match
the name of your step or any of the context keys that it utilizes.

## Split Steps
Sometimes you will have a pipeline step that will have a list of several values,
and you want to split the list so that each step will run once for each value. The split step
will perform the conversion of 1:X contexts after the step completes.

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
        # The pipeline will automatically split the first key listed in provides[].
        # For example, in the next step context.get('added_value') will return 0.
        # Then the next step will run again with the values 1, 2, 3, etc...
```

## Filter Steps
Filter steps have the option to pass back the value of `None`. If this is the case, this instance of the context will be deleted and not passed to the next step. Works great after split steps.

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
            context.set('filtered_value', value) # If the value is 1, pass it along to the next step.
        else:
            context.set('filtered_value', None) # If the value is zero, delete this context and don't pass it to the next step.
```

# Example Projects
- [RSSMQ](https://github.com/ARMmaster17/rssmq/tree/126-refactor-to-use-watergrid) - Forwards RSS feed items to various HTTP APIs.
- [atc-metrics-streamer](https://github.com/ARMmaster17/atc-metrics-streamer/tree/watergrid-transplant) - Streams metrics from Apache Traffic Control to Kafka.
