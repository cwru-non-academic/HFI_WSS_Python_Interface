class LogSink:
    def write(self, level: str, message: str) -> None:
        raise NotImplementedError("Provide a sink implementation.")
