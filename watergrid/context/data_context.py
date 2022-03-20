class DataContext():
    """
    Stores data from previous steps, and allows you to pass KV pairs to
    subsequent steps.
    """

    def __init__(self):
        self.data = {}

    def set(self, key: str, value: object) -> None:
        self.data[key] = value

    def get(self, key: str) -> object:
        return self.data[key]

    def has(self, key: str) -> bool:
        return key in self.data
