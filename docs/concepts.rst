Concepts
========

Pipeline
--------

A watergrid application is composed of a single pipeline, There are two types of pipelines:
- `StandalonePipeline` - For low impact use cases where simplicity is preferred.
- `HAPipeline` - For use cases where high availability is required along with only-once processing.

Steps
-----

A pipeline is composed of one or more steps. Once you create a pipeline, you can add steps using the `add_step()` method.
Watergrid expects that you create a new class for each step that you want to perform in the pipeline. All steps must
inherit from the abstract `Step` class. Your steps should provide an override for the `run(context)` method. Inside this
method you can perform any actions you want.

Context
-------

The context is a key-value store that is passed to each step in the pipeline. You can use the context to store
data created in your step, and to access data created in previous steps. Changing the `OutputMode` of the context
in a set allows for splitting or filtering the context after the step completes. This can be used to have subsequent
steps run multiple times based on the output of the current step.

Locks
-----

When using the `HAPipeline` class, you must provide a lock to prevent multiple instances from running the same pipeline
at the same time. The `RedisLock` class is provided by watergrid, but you are free to implement your own lock
using the `Lock` abstract class.