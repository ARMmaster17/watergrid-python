Working With Steps
==================

Custom Steps
------------

Every step of your pipeline should be its own class and inherit from the `Step` class. Here is an example:

.. code-block:: python

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

Note that the `requires` and `provides` lists are optional. If you do not specify them, the step will run
in any order in the pipeline. The keys provided in the two lists can be arbitrary, and do not need to match
the name of your step or any of the context keys that it utilizes.

Split Steps
-----------
Sometimes you will have a pipeline step that will have a list of several values,
and you want to split the list so that subsequent steps will run once for each value. The split step
will perform the conversion of 1:X contexts after the step completes.

.. code-block:: python

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

Filter Steps
------------
Filter steps have the option to pass back the value of `None`. If this is the case, this instance of the context will be deleted and not passed to the next step. Works great after split steps.

Note that the pipeline will only filter the first field listed in the provides list.

.. code-block:: python

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
