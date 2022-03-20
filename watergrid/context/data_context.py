from watergrid.context import OutputMode


class DataContext():
    """
    Stores data from previous steps, and allows you to pass KV pairs to
    subsequent steps.
    """

    def __init__(self):
        self.data = {}
        self.output_mode = OutputMode.DIRECT

    def set(self, key: str, value: object) -> None:
        self.data[key] = value

    def get(self, key: str) -> object:
        return self.data[key]

    def get_all(self) -> dict:
        return self.data

    def set_batch(self, batch: dict) -> None:
        self.data = batch

    def has(self, key: str) -> bool:
        return key in self.data

    def set_output_mode(self, mode: OutputMode) -> None:
        self.output_mode = mode

    def reset_context(self):
        self.output_mode = OutputMode.DIRECT

    def get_output_mode(self) -> OutputMode:
        return self.output_mode
