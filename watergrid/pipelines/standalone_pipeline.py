class StandalonePipeline:
    """
    A composable pipeline the runs on a single host. Provides no high availability or fault tolerance.

    :param name: The name of the pipeline.
    :type name: str
    """
    def __init__(self, name: str):
        self.__name = name

    def setup(self):
        """
        Setup the pipeline.
        """
        pass